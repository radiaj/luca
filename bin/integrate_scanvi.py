#!/usr/bin/env python
"""Run scANVI integration on prepared anndata object.

Usage ./integrate_scanpy.py adata.h5ad output_adata.h5ad model_out_dir
"""

import scanpy as sc
import numpy as np
import scvi
import sys

scvi.settings.seed = 0

adata_in = sys.argv[1]
adata_out = sys.argv[2]
model_out = sys.argv[3]
use_highly_variable = bool(int(sys.argv[4]))

adata = sc.read_h5ad(adata_in)

if use_highly_variable:
    sc.pp.highly_variable_genes(
        adata, flavor="seurat_v3", n_top_genes=6000, batch_key="dataset", subset=True
    )

scvi.data.setup_anndata(
    adata,
    batch_key="batch",
)

# lvae = scvi.model.SCANVI(adata, "unknown", use_cuda=True, n_latent=30, n_layers=2)
lvae = scvi.model.SCVI(adata)

lvae.train(
    use_gpu=True,
)
lvae.save(model_out)

# adata.obs["cell_type_predicted"] = lvae.predict(adata)
adata.obsm["X_scVI"] = lvae.get_latent_representation(adata)

adata.write_h5ad(adata_out)
