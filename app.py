import streamlit as st
from rdkit import Chem

# Set up page configurations
st.set_page_config(
    page_title="Chiral Center Finder",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Initialize session state for navigation tracking
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

# Navigation functions
def go_to_calculator():
    st.session_state.page = 'calculator'

def go_to_landing():
    st.session_state.page = 'landing'

# ==========================================
# PAGE 1: Landing Page
# ==========================================
if st.session_state.page == 'landing':
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #1f77b4;'>Chiral Center Finder<br><span style='color: #2c3e50;'>for Eribulin</span></h1>", unsafe_allow_html=True)
    st.markdown("<hr style='border:1px solid #e0e0e0;'>", unsafe_allow_html=True)
    
    # Student Details
    st.markdown("### 🎓 Student Details")
    st.markdown("""
    <div style='background-color:#f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #1f77b4; font-size: 18px;'>
        <b>Name:</b> SHANKAR S <br><br>
        <b>Register Number:</b> RA2511026050037 <br><br>
        <b>Course:</b> Chemistry Project
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Start Button (Centered)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.button("Start Project 🚀", on_click=go_to_calculator, use_container_width=True, type="primary")

# ==========================================
# PAGE 2: Main Application / Calculator
# ==========================================
elif st.session_state.page == 'calculator':
    
    # Back button
    st.button("← Back to Landing Page", on_click=go_to_landing)
    
    st.title("Eribulin Chiral Center Calculator")
    st.markdown("---")
    
    # Default Eribulin SMILES
    default_smiles = "C[C@@H]1C[C@@H]2CC[C@H]3C(=C)C[C@@H](O3)CC[C@]45C[C@@H]6[C@H](O4)[C@H]7[C@@H](O6)[C@@H](O7)CC[C@H]5[C@@H](C)O2"
    
    # Input configuration
    smiles_input = st.text_input("Enter a SMILES string below:", value=default_smiles)
    
    # Calculation logic
    if st.button("Calculate Chiral Centers", type="primary", use_container_width=True):
        if not smiles_input.strip():
            st.warning("Please enter a valid SMILES string.")
        else:
            with st.spinner('Extracting stereocenters...'):
                # Convert SMILES to RDKit Molecule object
                mol = Chem.MolFromSmiles(smiles_input)
                
                if mol is None:
                    # Handle invalid SMILES
                    st.error("Invalid SMILES string. Ensure the structure is correct.")
                else:
                    # Find chiral centers using RDKit
                    chiral_centers = Chem.FindMolChiralCenters(mol, includeUnassigned=True)
                    num_centers = len(chiral_centers)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Display results
                    st.success(f"### 🎉 Number of Chiral Centers: {num_centers}")
                    
                    if num_centers > 0:
                        st.write("**List of Chiral Centers (Atom Index, Stereochemistry):**")
                        
                        # Format chiral centers cleanly
                        center_data = [{"Atom Index": index, "Stereochemistry": stereo} for index, stereo in chiral_centers]
                        st.table(center_data)
                    else:
                        st.info("No chiral centers found in this molecule.")
                        
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; color: gray;'>Developed for Chemistry Project | SHANKAR S</div>", unsafe_allow_html=True)
