"""
XNRA Uncertainty Calculator v9
==============================
Calculates statistical uncertainties for IBA data from SIMNRA .xnra files.

This version implements the uncertainty formulas from the French IBA expert,
with proper separation of uncertainty components and optional χ²-adjustment.

VERSION 9 UPDATES:
- Added isotope-specific uncertainty calculations
- Clarified that Q·Ω and σ uncertainties are RELATIVE (constant across layers/elements)
- Isotopes can have different cross-section uncertainties based on their reactions
- Element spectrum parsing now preserves isotope data separately

=============================================================================
THEORETICAL BACKGROUND (from IBA-uncertainties-v3.pdf)
=============================================================================

1. DETECTED COUNTS RELATION
---------------------------
The number of detected counts for an element A can be expressed as:

    A_A = (Q · Ω · ∫[0→x] f · N_A(x) · σ_A(x) dx) / cos(α)

where:
- Q = collected charge
- Ω = detector solid angle  
- f = normalization factor
- N_A(x) = atomic concentration profile of element A
- σ_A(x) = reaction cross section
- α = incidence angle


2. STANDARD UNCERTAINTY ON CONCENTRATION (Equation 3)
-----------------------------------------------------
The uncertainty on concentration C_A combines independent uncertainties:

    ΔC_A = √[(ΔQΩ)² + (Δσ_A)² + (ΔA_A)²]

All terms are RELATIVE uncertainties (fractions, not absolute values).

IMPORTANT: ΔQΩ and Δσ are CONSTANT for all elements/layers in the same measurement.
Only ΔA_A (statistical) varies because it depends on element-specific counts.


3. χ²-ADJUSTED UNCERTAINTY (Equation 6)
---------------------------------------
When χ²/ν > 1, the statistical uncertainty may be underestimated. The
adjusted formula rescales the statistical term:

    ΔC_A^adj = √[(ΔQΩ)² + (Δσ_A)² + (√χ²/ν × ΔA_A)²]

This correction is only meaningful when χ²/ν significantly exceeds unity.
Otherwise, the standard expression should be used.


4. UNCERTAINTY COMPONENTS
-------------------------

a) ΔQΩ - Charge × Solid Angle Uncertainty (CONSTANT for all elements)
   - Estimated as standard deviation of ratios between simulated and 
     measured Particle·sr values during normalization
   - Valid for samples from the same analysis session
   - Typically 1-5% depending on setup stability
   - THIS IS A DETECTOR/SETUP PROPERTY - SAME FOR ALL ELEMENTS

b) Δσ_A - Cross-Section Uncertainty (varies by REACTION, not element)
   - Depends on the specific nuclear reaction:
     • 0%  for Mx(α,α)Mx (pure Rutherford backscattering)
     • ±2% for ¹⁶O(d,α₀)¹⁴N (deuteron NRA for oxygen)
     • ±2% for ¹H(⁴He,¹H)⁴He (forward recoil/ERDA for hydrogen)
     • ±5% for ¹²C(d,p₀)¹³C (deuteron NRA for carbon)
   - For isotope-specific calculations, each isotope may have different Δσ

c) ΔA_A - Statistical Uncertainty (Poisson) - VARIES by element
   - Given by: ΔA_A = √A_A / A_A = 1/√A_A
   - Where A_A = detected counts for element/isotope A at its reference peak
   - Calculated within a user-defined ROI (Region of Interest)


5. REDUCED CHI-SQUARED (χ²/ν)
-----------------------------
Defined as:

    χ²/ν = (1/ν) × Σ[(y_exp - y_sim)² / σ²]

where:
- y_exp, y_sim = experimental and simulated values
- σ = statistical uncertainty (√y_exp)
- ν = N - p = degrees of freedom (N = data points, p = fitted parameters)


=============================================================================
AUTHORS
=============================================================================
Based on work by Berke Santos & Giuseppe Legrottaglie
Formulas from French IBA expert documentation (v3)
Version 9: Isotope support + clarified constant Q·Ω/σ uncertainties

=============================================================================
"""

import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union
import re

# Import element spectrum functions from dedicated module
from .element_spectra import (
    get_available_elements,
    get_available_isotopes,
    get_element_spectrum_summary,
    plot_element_spectra,
    ELEMENT_COLORS,
)


# CROSS-SECTION UNCERTAINTIES (from IBA-uncertainties-v3.pdf)

CROSS_SECTION_UNCERTAINTIES = {
    # Reaction name: (uncertainty as fraction, description)
    # From IBA-uncertainties-v3.pdf (French IBA expert)
    'RBS: Mx(α,α)Mx': (0.00, 'Rutherford backscattering (pure Coulomb)'),
    'NRA: ¹⁶O(d,α₀)¹⁴N': (0.02, 'Deuteron NRA for oxygen'),
    'NRA: ¹²C(d,p₀)¹³C': (0.05, 'Deuteron NRA for carbon'),
    'NRA: ¹⁵N(p,αγ)¹²C': (0.03, 'Proton NRA for nitrogen'),
    'ERDA: ¹H(⁴He,¹H)⁴He': (0.02, 'Forward recoil for hydrogen'),
    'ERDA: ²H(⁴He,²H)⁴He': (0.03, 'Forward recoil for deuterium'),
}

# Default cross-section uncertainties by isotope (for common IBA scenarios)
# Users can override these in the GUI
ISOTOPE_CROSS_SECTION_DEFAULTS = {
    # Format: 'isotope': (default_uncertainty, default_reaction)
    # Hydrogen isotopes (typically ERDA)
    '1H': (0.02, 'ERDA: ¹H(⁴He,¹H)⁴He'),
    '2H': (0.03, 'ERDA: ²H(⁴He,²H)⁴He'),
    'H': (0.02, 'ERDA: ¹H(⁴He,¹H)⁴He'),
    
    # Carbon isotopes (NRA or RBS depending on setup)
    '12C': (0.05, 'NRA: ¹²C(d,p₀)¹³C'),
    '13C': (0.05, 'NRA: ¹²C(d,p₀)¹³C'),  # Same reaction uncertainty
    'C': (0.05, 'NRA: ¹²C(d,p₀)¹³C'),
    
    # Nitrogen isotopes
    '14N': (0.03, 'NRA: ¹⁵N(p,αγ)¹²C'),
    '15N': (0.03, 'NRA: ¹⁵N(p,αγ)¹²C'),
    'N': (0.03, 'NRA: ¹⁵N(p,αγ)¹²C'),
    
    # Oxygen isotopes (NRA or RBS)
    '16O': (0.02, 'NRA: ¹⁶O(d,α₀)¹⁴N'),
    '17O': (0.02, 'NRA: ¹⁶O(d,α₀)¹⁴N'),
    '18O': (0.02, 'NRA: ¹⁶O(d,α₀)¹⁴N'),
    'O': (0.02, 'NRA: ¹⁶O(d,α₀)¹⁴N'),
    
    # Heavy elements (typically RBS - Rutherford)
    # These have 0% cross-section uncertainty for pure Coulomb scattering
}

# Legacy mapping for backward compatibility
TECHNIQUE_TO_REACTION = {
    'RBS': 'RBS: Mx(α,α)Mx',
    'ERDA': 'ERDA: ¹H(⁴He,¹H)⁴He',
    'NRA': 'NRA: ¹²C(d,p₀)¹³C',  # Default NRA
}


def parse_xnra_full(filepath: str) -> Dict:
    """
    Parse .xnra file and extract all relevant data.
    
    The .xnra format is XML-based, following the IDF (Ion beam Data Format)
    schema with SIMNRA-specific extensions.
    
    Parameters
    ----------
    filepath : str
        Path to the .xnra file
    
    Returns
    -------
    dict
        Dictionary containing:
        - filepath, filename: File identification
        - layers: List of layer dicts with thickness and concentrations
        - raw_channels, raw_counts: Experimental spectrum
        - simulated_channels, simulated_counts: Fitted/simulated spectrum
        - beam_energy, beam_particle, scattering_angle: Experimental setup
        - cal_offset, cal_gain: Energy calibration (E = offset + gain × channel)
    """
    tree = ET.parse(filepath)
    root = tree.getroot()
    
    ns = {
        'idf': 'http://idf.schemas.itn.pt',
        'simnra': 'http://www.simnra.com/simnra'
    }
    
    data = {
        'filepath': str(filepath),
        'filename': Path(filepath).stem,
        'layers': [],
        'elements': [],
        'raw_channels': None,
        'raw_counts': None,
        'simulated_channels': None,
        'simulated_counts': None,
        'beam_energy': None,
        'beam_particle': None,
        'scattering_angle': None,
        'cal_offset': 0,
        'cal_gain': 1,
    }
    
    beam_particle = root.find('.//idf:beamparticle', ns)
    if beam_particle is not None:
        data['beam_particle'] = beam_particle.text
    
    beam_energy = root.find('.//idf:beamenergy', ns)
    if beam_energy is not None:
        data['beam_energy'] = float(beam_energy.text)
    
    scattering_angle = root.find('.//idf:scatteringangle', ns)
    if scattering_angle is not None:
        data['scattering_angle'] = float(scattering_angle.text)
    
    cal_params = root.findall('.//idf:energycalibration[1]/idf:calibrationparameters/idf:calibrationparameter', ns)
    if len(cal_params) >= 2:
        data['cal_offset'] = float(cal_params[0].text)
        data['cal_gain'] = float(cal_params[1].text)
    
    elements = root.findall('.//idf:elementsandmolecules/idf:elements/idf:element/idf:n', ns)
    data['elements'] = [el.text for el in elements]
    
    layers = root.findall('.//idf:layeredstructure/idf:layers/idf:layer', ns)
    
    for i, layer in enumerate(layers):
        layer_data = {
            'layer_num': i + 1,
            'thickness': None,
            'concentrations': {},
            'isotope_concentrations': {},  # NEW: Keep isotope-specific data
        }
        
        # Thickness (in 10^15 atoms/cm²)
        thickness_el = layer.find('idf:layerthickness', ns)
        if thickness_el is not None:
            layer_data['thickness'] = float(thickness_el.text)
        
        # Element concentrations
        layer_elements = layer.findall('.//idf:layerelement', ns)
        for el in layer_elements:
            name_el = el.find('idf:name', ns)
            if name_el is None:
                name_el = el.find('idf:n', ns)
            conc_el = el.find('idf:concentration', ns)
            
            if name_el is not None and conc_el is not None:
                element_name = name_el.text
                concentration = float(conc_el.text)
                
                # Store isotope-specific concentration
                layer_data['isotope_concentrations'][element_name] = concentration
                
                # Also store summed element concentration (backward compatible)
                # Normalize isotope names (e.g., "40Ca" -> "Ca")
                base_element = re.sub(r'^\d+', '', element_name)
                
                # Sum isotopes for the same element
                if base_element in layer_data['concentrations']:
                    layer_data['concentrations'][base_element] += concentration
                else:
                    layer_data['concentrations'][base_element] = concentration
        
        data['layers'].append(layer_data)
    
    raw_data = root.find('.//idf:data/idf:simpledata', ns)
    if raw_data is not None:
        x_el = raw_data.find('idf:x', ns)
        y_el = raw_data.find('idf:y', ns)
        if x_el is not None and y_el is not None:
            data['raw_channels'] = np.array([float(x) for x in x_el.text.split()])
            data['raw_counts'] = np.array([float(y) for y in y_el.text.split()])
    
    sim_data = root.find('.//idf:simulation[1]/idf:simpledata', ns)
    if sim_data is None:
        sim_data = root.find('.//simnra:calculateddata/idf:simpledata', ns)
    
    if sim_data is not None:
        x_el = sim_data.find('idf:x', ns)
        y_el = sim_data.find('idf:y', ns)
        if x_el is not None and y_el is not None:
            data['simulated_channels'] = np.array([float(x) for x in x_el.text.split()])
            data['simulated_counts'] = np.array([float(y) for y in y_el.text.split()])
    
    return data


# UNCERTAINTY CALCULATIONS (v9 - French Expert Formulas + Isotope Support)

def calculate_chi_squared_for_roi(raw_counts: np.ndarray, 
                                   simulated_counts: np.ndarray,
                                   roi_start: int,
                                   roi_end: int,
                                   min_counts: float = 4.0,
                                   n_params: int = 1) -> Tuple[float, int, int, float]:
    """
    Calculate reduced chi-squared and AUC ratio for a specific ROI.
    
    Formula (Equation 5 from IBA-uncertainties-v3.pdf):
    
        χ²/ν = (1/ν) × Σ[(y_exp - y_sim)² / σ²]
    
    where:
    - y_exp, y_sim = experimental and simulated values
    - σ = √(max(y_exp, min_counts)) = Poisson uncertainty
    - ν = N - p = degrees of freedom
    
    Also calculates AUC ratio = Σ(y_sim) / Σ(y_exp) for normalization check.
    
    Parameters
    ----------
    raw_counts : np.ndarray
        Experimental spectrum counts (y_exp)
    simulated_counts : np.ndarray
        Simulated/fitted spectrum counts (y_sim)
    roi_start : int
        Start channel of ROI (inclusive)
    roi_end : int
        End channel of ROI (exclusive)
    min_counts : float, default=4.0
        Minimum counts for uncertainty calculation (avoids division by zero)
    n_params : int, default=1
        Number of fitted parameters (p) for degrees of freedom calculation
    
    Returns
    -------
    tuple
        (chi2_reduced, degrees_of_freedom, total_counts_in_roi, auc_ratio)
    """
    # Ensure bounds are valid
    roi_start = max(0, roi_start)
    roi_end = min(roi_end, len(raw_counts), len(simulated_counts))
    
    if roi_start >= roi_end:
        return np.nan, 0, 0, np.nan
    
    # Extract ROI
    raw_roi = raw_counts[roi_start:roi_end]
    sim_roi = simulated_counts[roi_start:roi_end]
    
    if len(raw_roi) == 0:
        return np.nan, 0, 0, np.nan
    
    # Total counts in ROI (for counting statistics)
    total_counts = int(np.sum(raw_roi))
    total_sim_counts = np.sum(sim_roi)
    
    # AUC ratio: simple normalization check
    auc_ratio = total_sim_counts / total_counts if total_counts > 0 else np.nan
    
    # Poisson uncertainty: σ = √N, with minimum to avoid div/0
    sigma = np.sqrt(np.maximum(raw_roi, min_counts))
    
    # Chi-squared: Σ[(y_exp - y_sim)² / σ²]
    chi2 = np.sum((raw_roi - sim_roi)**2 / sigma**2)
    
    # Degrees of freedom: ν = N - p
    n_points = len(raw_roi)
    dof = n_points - n_params
    
    chi2_reduced = chi2 / dof if dof > 0 else np.inf
    
    return chi2_reduced, dof, total_counts, auc_ratio


def interpret_chi2(chi2_reduced: float) -> Tuple[str, str]:
    """
    Interpret the reduced chi-squared value.
    
    Parameters
    ----------
    chi2_reduced : float
        The reduced chi-squared value
    
    Returns
    -------
    tuple
        (status_symbol, description)
    """
    if np.isnan(chi2_reduced):
        return "?", "N/A"
    elif 0.90 <= chi2_reduced <= 1.10:
        return "✓✓", "Perfect"
    elif 1.10 < chi2_reduced <= 3.0:
        return "✓", "Great"
    elif 3.0 < chi2_reduced <= 10.0:
        return "⚠", "Not OK"
    elif chi2_reduced > 10.0:
        return "✗", "Very bad"
    elif chi2_reduced < 0.90:
        return "⚠", "Too low"
    else:
        return "?", "Unknown"


# NOTE: Element spectrum functions live in flavunato/element_spectra.py
# Import: parse_element_spectrum, get_element_spectrum_summary, 
#         plot_element_spectra, calculate_element_counts_from_spectrum, etc.


def get_isotope_cross_section_uncertainty(isotope: str, 
                                           custom_overrides: Dict[str, float] = None) -> Tuple[float, str]:
    """
    Get the cross-section uncertainty for a specific isotope.
    
    Parameters
    ----------
    isotope : str
        Isotope name (e.g., '12C', '16O', 'H')
    custom_overrides : dict, optional
        Dict mapping isotope name → uncertainty (as fraction)
    
    Returns
    -------
    tuple
        (uncertainty as fraction, reaction description)
    """
    # Check custom overrides first
    if custom_overrides and isotope in custom_overrides:
        return custom_overrides[isotope], 'Custom'
    
    # Check default isotope uncertainties
    if isotope in ISOTOPE_CROSS_SECTION_DEFAULTS:
        unc, reaction = ISOTOPE_CROSS_SECTION_DEFAULTS[isotope]
        return unc, reaction
    
    # Try stripping mass number to find element default
    base_element = re.sub(r'^\d+', '', isotope)
    if base_element in ISOTOPE_CROSS_SECTION_DEFAULTS:
        unc, reaction = ISOTOPE_CROSS_SECTION_DEFAULTS[base_element]
        return unc, reaction
    
    # Default to Rutherford (0% uncertainty for heavy elements)
    return 0.0, 'RBS: Mx(α,α)Mx'


def calculate_uncertainty_v9(concentration: float,
                              element_counts: int,
                              qomega_uncertainty: float,
                              cross_section_uncertainty: float,
                              chi2_reduced: float = 1.0,
                              auc_ratio: float = 1.0,
                              adjustment_method: str = 'none') -> Dict[str, float]:
    """
    Calculate uncertainties using the French expert's formulas (v9).
    
    Standard Formula (Equation 3):
    ------------------------------
        ΔC_A = √[(ΔQΩ)² + (Δσ_A)² + (ΔA_A)²]
    
    IMPORTANT: ΔQΩ and Δσ_A are RELATIVE uncertainties that are CONSTANT
    for all elements/layers. Only ΔA_A varies based on counting statistics.
    
    Parameters
    ----------
    concentration : float
        Element concentration as a fraction (0 to 1, not percentage)
    element_counts : int
        Number of detected counts for element A in the ROI (A_A)
    qomega_uncertainty : float
        Q·Ω uncertainty as fraction (e.g., 0.03 for 3%) - CONSTANT for all elements
    cross_section_uncertainty : float
        Cross-section uncertainty as fraction (e.g., 0.02 for 2%) - per reaction
    chi2_reduced : float, default=1.0
        Reduced chi-squared value for the ROI
    auc_ratio : float, default=1.0
        AUC ratio (Σsim/Σexp) for the ROI
    adjustment_method : str, default='none'
        Which adjustment to apply: 'none', 'chi2', or 'auc'
    
    Returns
    -------
    dict
        Contains standard and all adjusted uncertainties for comparison.
        
        KEY DISTINCTION:
        - sigma_*_rel: RELATIVE uncertainties (fractions) - use for display
        - sigma_*: ABSOLUTE uncertainties (fractions of concentration)
    """
    # Statistical uncertainty (Poisson): ΔA_A = 1/√A_A
    if element_counts > 0:
        sigma_stat_rel = 1.0 / np.sqrt(element_counts)
    else:
        sigma_stat_rel = np.nan
    
    # Store relative uncertainties - THESE ARE CONSTANT (except stat)
    sigma_qomega_rel = qomega_uncertainty   # CONSTANT - detector property
    sigma_xsec_rel = cross_section_uncertainty  # CONSTANT per reaction type
    
    # χ² adjustment factor: √(max(χ²/ν, 1))
    if not np.isnan(chi2_reduced):
        chi2_factor = np.sqrt(max(chi2_reduced, 1.0))
    else:
        chi2_factor = 1.0
    
    # AUC adjustment factor: max(AUC, 1/AUC)
    if not np.isnan(auc_ratio) and auc_ratio > 0:
        auc_factor = max(auc_ratio, 1.0 / auc_ratio)
    else:
        auc_factor = 1.0
    
    # Calculate all versions of statistical uncertainty (relative)
    if not np.isnan(sigma_stat_rel):
        sigma_stat_chi2_rel = chi2_factor * sigma_stat_rel
        sigma_stat_auc_rel = auc_factor * sigma_stat_rel
    else:
        sigma_stat_chi2_rel = np.nan
        sigma_stat_auc_rel = np.nan
    
    # Standard combined RELATIVE uncertainty (Equation 3)
    if not np.isnan(sigma_stat_rel):
        sigma_total_rel = np.sqrt(
            sigma_qomega_rel**2 + 
            sigma_xsec_rel**2 + 
            sigma_stat_rel**2
        )
    else:
        sigma_total_rel = np.sqrt(sigma_qomega_rel**2 + sigma_xsec_rel**2)
    
    # χ²-adjusted combined uncertainty (Equation 6)
    if not np.isnan(sigma_stat_chi2_rel):
        sigma_total_chi2_rel = np.sqrt(
            sigma_qomega_rel**2 + 
            sigma_xsec_rel**2 + 
            sigma_stat_chi2_rel**2
        )
    else:
        sigma_total_chi2_rel = np.sqrt(sigma_qomega_rel**2 + sigma_xsec_rel**2)
    
    # AUC-adjusted combined uncertainty
    if not np.isnan(sigma_stat_auc_rel):
        sigma_total_auc_rel = np.sqrt(
            sigma_qomega_rel**2 + 
            sigma_xsec_rel**2 + 
            sigma_stat_auc_rel**2
        )
    else:
        sigma_total_auc_rel = np.sqrt(sigma_qomega_rel**2 + sigma_xsec_rel**2)
    
    # Convert to absolute uncertainties (scaled by concentration)
    # These represent the actual uncertainty in concentration percentage
    sigma_stat_abs = concentration * sigma_stat_rel if not np.isnan(sigma_stat_rel) else np.nan
    sigma_stat_chi2_abs = concentration * sigma_stat_chi2_rel if not np.isnan(sigma_stat_chi2_rel) else np.nan
    sigma_stat_auc_abs = concentration * sigma_stat_auc_rel if not np.isnan(sigma_stat_auc_rel) else np.nan
    sigma_qomega_abs = concentration * sigma_qomega_rel
    sigma_xsec_abs = concentration * sigma_xsec_rel
    sigma_total_abs = concentration * sigma_total_rel
    sigma_total_chi2_abs = concentration * sigma_total_chi2_rel
    sigma_total_auc_abs = concentration * sigma_total_auc_rel
    
    # Choose which to report based on adjustment method
    if adjustment_method == 'chi2':
        sigma_stat_final_abs = sigma_stat_chi2_abs
        sigma_stat_final_rel = sigma_stat_chi2_rel
        sigma_total_final_abs = sigma_total_chi2_abs
        sigma_total_final_rel = sigma_total_chi2_rel
        adjustment_factor = chi2_factor
    elif adjustment_method == 'auc':
        sigma_stat_final_abs = sigma_stat_auc_abs
        sigma_stat_final_rel = sigma_stat_auc_rel
        sigma_total_final_abs = sigma_total_auc_abs
        sigma_total_final_rel = sigma_total_auc_rel
        adjustment_factor = auc_factor
    else:  # 'none' or default
        sigma_stat_final_abs = sigma_stat_abs
        sigma_stat_final_rel = sigma_stat_rel
        sigma_total_final_abs = sigma_total_abs
        sigma_total_final_rel = sigma_total_rel
        adjustment_factor = 1.0
    
    return {
        # PRIMARY UNCERTAINTIES (based on selected method)
        # Absolute (concentration-scaled)
        'sigma_stat': sigma_stat_final_abs,
        'sigma_qomega': sigma_qomega_abs,
        'sigma_xsec': sigma_xsec_abs,
        'sigma_total': sigma_total_final_abs,
        
        # Relative (CONSTANT for Q·Ω and σ) - USE THESE FOR DISPLAY
        'sigma_stat_rel': sigma_stat_final_rel,
        'sigma_qomega_rel': sigma_qomega_rel,  # CONSTANT
        'sigma_xsec_rel': sigma_xsec_rel,       # CONSTANT
        'sigma_total_rel': sigma_total_final_rel,
        
        # ALL VERSIONS FOR COMPARISON (absolute)
        'sigma_stat_standard': sigma_stat_abs,
        'sigma_stat_chi2_adjusted': sigma_stat_chi2_abs,
        'sigma_stat_auc_adjusted': sigma_stat_auc_abs,
        'sigma_total_standard': sigma_total_abs,
        'sigma_total_chi2_adjusted': sigma_total_chi2_abs,
        'sigma_total_auc_adjusted': sigma_total_auc_abs,
        
        # All versions (relative)
        'sigma_stat_standard_rel': sigma_stat_rel,
        'sigma_stat_chi2_adjusted_rel': sigma_stat_chi2_rel,
        'sigma_stat_auc_adjusted_rel': sigma_stat_auc_rel,
        'sigma_total_standard_rel': sigma_total_rel,
        'sigma_total_chi2_adjusted_rel': sigma_total_chi2_rel,
        'sigma_total_auc_adjusted_rel': sigma_total_auc_rel,
        
        'chi2_factor': chi2_factor,
        'auc_factor': auc_factor,
        'adjustment_factor': adjustment_factor,
        'adjustment_method': adjustment_method,
    }


def get_cross_section_uncertainty(reaction: str) -> float:
    """
    Get the cross-section uncertainty for a given reaction.
    
    Parameters
    ----------
    reaction : str
        Reaction name (must match keys in CROSS_SECTION_UNCERTAINTIES)
        or a technique name ('RBS', 'ERDA', 'NRA')
    
    Returns
    -------
    float
        Cross-section uncertainty as a fraction
    """
    # Direct lookup
    if reaction in CROSS_SECTION_UNCERTAINTIES:
        return CROSS_SECTION_UNCERTAINTIES[reaction][0]
    
    # Technique mapping
    if reaction.upper() in TECHNIQUE_TO_REACTION:
        mapped_reaction = TECHNIQUE_TO_REACTION[reaction.upper()]
        return CROSS_SECTION_UNCERTAINTIES[mapped_reaction][0]
    
    # Default fallback
    return 0.05


def create_depth_profile(df: pd.DataFrame,
                          sample_name: str = None,
                          elements_order: List[str] = None,
                          adjustment_method: str = 'none') -> pd.DataFrame:
    """
    Create a depth profile table from uncertainty results.
    """
    if df.empty:
        return pd.DataFrame()
    
    if sample_name:
        df = df[df['filename'] == sample_name]
    
    if df.empty:
        return pd.DataFrame()
    
    layers = sorted(df['layer'].unique())
    
    if elements_order is None:
        elements_order = sorted(df['element'].unique())
    else:
        elements_order = [e for e in elements_order if e in df['element'].unique()]
    
    unc_col_map = {
        'none': 'sigma_total_standard_percent',
        'chi2': 'sigma_total_chi2_adjusted_percent',
        'auc': 'sigma_total_auc_adjusted_percent'
    }
    unc_col = unc_col_map.get(adjustment_method, 'sigma_total_percent')
    if unc_col not in df.columns:
        unc_col = 'sigma_total_percent'
    
    thickness_col = None
    for col_name in ['thickness_1e15_at_cm2', 'thickness']:
        if col_name in df.columns:
            thickness_col = col_name
            break
    
    rows = []
    for layer_num in layers:
        layer_df = df[df['layer'] == layer_num]
        
        thickness = None
        if thickness_col and len(layer_df) > 0:
            thickness = layer_df[thickness_col].iloc[0]
        
        row = {
            'Layer': layer_num,
            'Thickness (10¹⁵ at/cm²)': thickness,
        }
        
        for element in elements_order:
            el_df = layer_df[layer_df['element'] == element]
            
            if len(el_df) > 0:
                best_idx = el_df['chi2_reduced'].idxmin()
                best = el_df.loc[best_idx]
                
                row[f'{element} (%)'] = round(best['concentration_percent'], 2)
                row[f'±{element} (%)'] = round(best[unc_col], 3)
            else:
                row[f'{element} (%)'] = None
                row[f'±{element} (%)'] = None
        
        rows.append(row)
    
    return pd.DataFrame(rows)
