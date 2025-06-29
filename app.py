import os
import streamlit as st
import pandas as pd
import gdown
import joblib

# ---------- MODEL LOADING ----------
@st.cache_resource
def download_file_from_drive(file_id, output):
    if not os.path.exists(output):
        st.info(f"Downloading {output} ...")
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, output, quiet=False)


download_file_from_drive("15NY4RXXX7AleM2xV87G2n5h1T2Voiozj", "final_pipelineY.pkl")


def load_model():
    with open("final_pipelineY.pkl", "rb") as f:
        return joblib.load(f)

model=load_model()


st.title("Gene Mutation Classifier")

# ---------- FEATURE LISTS ----------
all_cols = [
    'CHROM', 'POS', 'REF', 'ALT', 'AF_ESP', 'AF_EXAC', 'AF_TGP', 'CLNDISDB',
    'CLNDN', 'CLNHGVS', 'CLNVC', 'MC', 'ORIGIN', 'CLASS', 'Allele',
    'Consequence', 'IMPACT', 'SYMBOL', 'Feature_type', 'Feature', 'BIOTYPE',
    'EXON', 'cDNA_position', 'CDS_position', 'Protein_position',
    'Amino_acids', 'Codons', 'STRAND', 'BAM_EDIT', 'SIFT', 'PolyPhen',
    'LoFtool', 'CADD_PHRED', 'CADD_RAW', 'BLOSUM62'
]
target = "PolyPhen"

numerical_cols = [
    'POS', 'AF_ESP', 'AF_EXAC', 'AF_TGP', 'ORIGIN', 'CLASS', 'STRAND',
    'LoFtool', 'CADD_PHRED', 'CADD_RAW', 'BLOSUM62'
]
categorical_cols = [c for c in all_cols if c not in numerical_cols and c != target]
input_cols = [c for c in all_cols if c != target]  # everything except the label

# ---------- UI  ----------
inputs = {}

st.header("Numerical features")
for col in numerical_cols:
    inputs[col] = st.number_input(col, value=0.0, format="%.6f")

st.header("Categorical features")
for col in categorical_cols:
    inputs[col] = st.text_input(col, "")

# ---------- PREDICTION ----------
if st.button("Predict"):
    input_df = pd.DataFrame([inputs])[input_cols]

    if model is not None:
        pred = model.predict(input_df)[0]
        prob = model.predict_proba(input_df).max()

        label = "benign" if pred == 0 else "pathogenic"
        st.subheader("Prediction")
        st.write(f"**PolyPhen class:** {label}")
        st.write(f"**Confidence:** {prob:.2%}")
    else:
        st.error("Model not loaded — check the file path or format.")

