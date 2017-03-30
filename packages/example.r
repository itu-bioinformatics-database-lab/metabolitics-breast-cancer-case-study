library(pathifier)

# 4 metabolites and 8 subjects/samples
metabolite_fold_changes = cbind(c(1.2, 2.5, 0.6, 1.0), c(0.5, 2.1, 0.8, 1.5),
                                c(1.2, 2.5, 0.6, 1.0), c(0.5, 2.1, 0.8, 1.5),
                                c(5.1, 3.2, 8.4, 4.5), c(4.6, 2.9, 10.1, 5.2),
                                c(5.1, 3.2, 8.4, 4.5), c(4.6, 2.9, 10.1, 5.2))

all_metabolite_ids = c('gal_c', 'Lcystin_c', 'pi_x', 'asn_L_c')

pathway_metabolites = list(c('gal_c', 'Lcystin_c', 'pi_x', 'asn_L_c'),
                           c('Lcystin_c', 'pi_x', 'asn_L_c'),
                           c('gal_c', 'pi_x', 'asn_L_c'))

pathway_names = c('pathway1', 'pathway2', 'pathway3')

is_healthy = c(TRUE, TRUE, TRUE, TRUE, FALSE, FALSE, FALSE, FALSE)

PDS<-quantify_pathways_deregulation(metabolite_fold_changes,
                                    all_metabolite_ids,
                                    pathway_metabolites, pathway_names,
                                    is_healthy, attempts = 100,
                                    min_exp=0, min_std=0)

x<-NULL
x$normals<-PDS$scores$pathway1[is_healthy]
x$tumors<-PDS$scores$pathway2[!is_healthy]
print(typeof(PDS))
boxplot(x)
boxplot(x,ylab="score")

print(x)
print(PDS$scores)
