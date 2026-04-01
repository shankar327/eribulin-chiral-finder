import streamlit as st
from rdkit import Chem
from rdkit.Chem import Draw

# Set up page configurations
st.set_page_config(
    page_title="Chiral Center Finder",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Initialize navigation
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

def go_to_calculator():
    st.session_state.page = 'calculator'

def go_to_landing():
    st.session_state.page = 'landing'

# ==========================================
# PAGE 1: Formal Project Cover Page
# ==========================================
if st.session_state.page == 'landing':
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # Very formal, academic styled cover page
    st.markdown("""
        <div style="border: 3px solid #1f77b4; padding: 40px; border-radius: 15px; background-color: #fcfcfc; text-align: center; box-shadow: 2px 5px 15px rgba(0,0,0,0.1);">
            <h2 style="color: #6c757d; text-transform: uppercase; font-size: 1.2rem; letter-spacing: 2px;">Chemistry Project Submission</h2>
            <br>
            <h1 style="color: #1f77b4; font-size: 2.8rem; margin: 10px 0;">Chiral Center Finder</h1>
            <h2 style="color: #2c3e50; font-size: 1.8rem;">Topic: Eribulin</h2>
            
            <hr style="border:1px solid #e0e0e0; margin: 30px 0;">
            
            <div style="text-align: left; max-width: 350px; margin: 0 auto; font-size: 1.3rem; line-height: 1.8;">
                <b>Name:</b> SHANKAR S <br>
                <b>Register Number:</b> RA2511026050037 <br>
            </div>
            <br>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.button("Start Project Application 🚀", on_click=go_to_calculator, use_container_width=True, type="primary")

# ==========================================
# PAGE 2: Advanced Calculator UI
# ==========================================
elif st.session_state.page == 'calculator':
    
    st.button("← Back to Cover Page", on_click=go_to_landing)
    
    st.markdown("<h2 style='text-align: center; color: #1f77b4;'>Eribulin Chiral Center Calculator</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    default_smiles = "C[C@@H]1C[C@@H]2CC[C@H]3C(=C)C[C@@H](O3)CC[C@]45C[C@@H]6[C@H](O4)[C@H]7[C@@H](O6)[C@@H](O7)CC[C@H]5[C@@H](C)O2"
    
    smiles_input = st.text_input("Enter a SMILES string below:", value=default_smiles)
    
    if st.button("Calculate Chiral Centers", type="primary", use_container_width=True):
        if not smiles_input.strip():
            st.warning("Please enter a valid SMILES string.")
        else:
            with st.spinner('Extracting stereocenters and generating 2D model...'):
                mol = Chem.MolFromSmiles(smiles_input)
                
                if mol is None:
                    st.error("Invalid SMILES string. Ensure the chemical structure is correct.")
                else:
                    chiral_centers = Chem.FindMolChiralCenters(mol, includeUnassigned=True)
                    num_centers = len(chiral_centers)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Dashboard Layout: Left side molecule image, Right side Metrics
                    col1, col2 = st.columns([1, 1.2])
                    
                    with col1:
                        st.markdown("**2D Molecular Structure:**")
                        try:
                            # Generate a beautiful 2D Image of the molecule
                            img = Draw.MolToImage(mol, size=(300, 300))
                            st.image(img, use_container_width=True)
                        except Exception:
                            st.info("Could not render 2D image for this structure.")
                            
                    with col2:
                        # Massive KPI Card for the number
                        st.markdown(f"""
                            <div style="background-color: #d1fae5; padding: 20px; border-radius: 10px; border-left: 5px solid #10b981; text-align: center;">
                                <h3 style="margin:0; color: #065f46;">Total Chiral Centers</h3>
                                <h1 style="margin:0; font-size: 3rem; color: #047857;">{num_centers}</h1>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        if num_centers > 0:
                            st.write("**List of Chiral Centers (Atom Index, Stereochemistry):**")
                            # Format chiral centers explicitly for the table
                            center_data = [{"Atom Index": index, "Stereochemistry": stereo} for index, stereo in chiral_centers]
                            st.dataframe(center_data, use_container_width=True, hide_index=True)
                        else:
                            st.info("No chiral centers found in this molecule.")
                        
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; color: gray; font-size: 14px;'>Developed for Chemistry Project | SHANKAR S</div>", unsafe_allow_html=True)

