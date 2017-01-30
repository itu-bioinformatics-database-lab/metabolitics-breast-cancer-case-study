library(pathifier)

data(Sheffer)

data(KEGG)

# args <- commandArgs(trailingOnly = TRUE)

PDS <- quantify_pathways_deregulation(sheffer$data, sheffer$allgenes,
    kegg$gs, kegg$pathwaynames, sheffer$normals, attempts = 100,
    min_exp=sheffer$minexp, min_std=sheffer$minstd)

# cat(PDS$scores$MISMATCH_REPAIR)
