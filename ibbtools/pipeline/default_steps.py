import re
from collections import defaultdict
from flask import current_app as app

from ibbtools.pipeline.repo import Step
import ibbtools.pipeline.services as services


# Input Output
TC_ID = 'TC'

DM_ID = 'FBgn'
DM_SYMBOL = 'FB symbol'
DM_NAME = 'FB name'
DM_CG = 'CG'

# GO_ID = 'GO ID'
# GO_ASPECT = 'GO aspect'
# GO_TERM = 'GO term'

IB_ID = 'iB'

LETHALITY_LARVAL_11 = 'larval lethality day 11'
LETHALITY_LARVAL_22 = 'larval lethality day 22'
LETHALITY_PUPAL_11 = 'pupal lethality day 11'

# Category
CAT_GENE_ALIAS = 'Gene Alias'
CAT_GENE_FUNCTION = 'Gene Function'
CAT_ORTHOLOGY = 'Orthology'


def get_default_steps(version=None):
    genomics_base_url = app.config['GENOMICSSERVICE_BASE_URL']
    main_species = app.config['MAIN_SPECIES']
    ortholog_species = app.config['ORTHOLOG_SPECIES']
    orthology_source = app.config['ORTHOLOGY_SOURCE']
    genomics_version = (
            app.config['GENOMICS_VERSION'] if version is None else version)

    geneinfo_service = services.GeneInfoService(
            genomics_base_url,
            species=ortholog_species,
            version=genomics_version)

    orthology_service = services.OrthologyService(
            genomics_base_url,
            main_species=main_species,
            reference_species=ortholog_species,
            source=orthology_source,
            version=genomics_version)

    genesilencing_service = services.GeneSilencingService(
            genomics_base_url,
            species=main_species,
            version=genomics_version)

#     geneontology_service = services.GeneOntologyService(
#             app.config['GENEONTOLOGY_SERVICE_BASE_URL'])

    phenotypeservice = services.PhenotypeService(
            app.config['PHENOTYPESERVICE_BASE_URL'])

    main_gene_pattern = re.compile(
            app.config['MAIN_SPECIES_GENE_PATTERN'])
    ortholog_gene_pattern = re.compile(
            app.config['ORTHOLOG_SPECIES_GENE_PATTERN'])


    def func__dm_id__dm_symbol(dm_id_list):
        genes = geneinfo_service.get_drosophila_genes(dm_id_list)
        return {gene['id']: [gene.get('symbol')] for gene in genes}

    step__dm_id__dm_symbol = Step(DM_ID, DM_SYMBOL,
            category=CAT_GENE_ALIAS,
            convert_func=func__dm_id__dm_symbol,
            description='Convert Drosophila gene identifiers in FBgnxxxxxxx'
            ' format to their corresponding symbol')


    def func__dm_id__dm_name(dm_id_list):
        genes = geneinfo_service.get_drosophila_genes(dm_id_list)
        return {gene['id']: [gene.get('fullname')] for gene in genes}


    step__dm_id__dm_name = Step(DM_ID, DM_NAME,
            category=CAT_GENE_ALIAS,
            convert_func=func__dm_id__dm_name,
            description='Convert Drosophila gene identifiers in FBgnxxxxxxx'
            ' format to their corresponding name')


    def func__dm_id__dm_cg(dm_id_list):
        genes = geneinfo_service.get_drosophila_genes(dm_id_list)
        return {gene['id']: [gene.get('annotationId')] for gene in genes}

    step__dm_id__dm_cg = Step(DM_ID, DM_CG,
            category=CAT_GENE_ALIAS,
            convert_func=func__dm_id__dm_cg,
            description='Convert Drosophila gene identifiers in FBgnxxxxxxx'
            ' format to CGxxxx format')


    def func__dm_symbol__dm_id(dm_symbol_list):
        mapping = {}
        for symbol in dm_symbol_list:
            genes = geneinfo_service.get_drosophila_genes(symbol=symbol)
            gene_ids = [gene['id'] for gene in genes]
            mapping[symbol] = gene_ids

        return mapping

    step__dm_symbol__dm_id = Step(DM_SYMBOL, DM_ID,
            category=CAT_GENE_ALIAS,
            convert_func=func__dm_symbol__dm_id,
            description='Convert Drosophila symbols to their gene identifiers'
            ' in FBgnxxxxxxx format')


    def func__dm_cg__dm_id(dm_cg_list):
        mapping = {}
        for cg in dm_cg_list:
            genes = geneinfo_service.get_drosophila_genes(cg=cg)
            gene_ids = [gene['id'] for gene in genes]
            mapping[cg] = gene_ids

        return mapping


    step__dm_cg__dm_id = Step(DM_CG, DM_ID,
            category=CAT_GENE_ALIAS,
            convert_func=func__dm_cg__dm_id,
            description='Convert Drosophila gene identifiers in CGxxxx format'
            ' to FBgnxxxxxxx format')

    def func__tc_id__dm_id(tc_id_list):
        orthologs = orthology_service.get_tribolium_orthologs(tc_id_list)
        mapping = {}
        for ortholog in orthologs:
            mapping[ortholog['gene']] = [
                o['gene'] for o in ortholog.get('orthologs', [])
                if ortholog_gene_pattern.match(o['gene'])
            ]
        return mapping

    step__tc_id__dm_id = Step(TC_ID, DM_ID,
            category=CAT_ORTHOLOGY,
            convert_func=func__tc_id__dm_id,
            description='Get Drosophila orthologs for Tribolium genes using OrthoFinder')


    def func__dm_id__tc_id(dm_id_list):
        orthologs = orthology_service.get_drosophila_orthologs(dm_id_list)
        mapping = {}
        for ortholog in orthologs:
            mapping[ortholog['gene']] = [
                o['gene'] for o in ortholog.get('orthologs', [])
                if main_gene_pattern.match(o['gene'])
            ]
        return mapping

    step__dm_id__tc_id = Step(DM_ID, TC_ID,
            category=CAT_ORTHOLOGY,
            convert_func=func__dm_id__tc_id,
            description='Get Tribolium orthologs for Drosophila genes using OrthoFinder')


    def func__tc_id__ib_id(tc_id_list):
        fragments = genesilencing_service.get_silencing_fragments(
                tc_id_list=tc_id_list)

        mapping = defaultdict(list)
        for fragment in fragments:
            ib_id = fragment['id']
            for tc_id in fragment.get('geneIds', []):
                mapping[tc_id].append(ib_id)
        return mapping

    step__tc_id__ib_id = Step(TC_ID, IB_ID,
            category=CAT_GENE_FUNCTION,
            convert_func=func__tc_id__ib_id,
            description='Get iB numbers for Tribolium genes')


    def func__ib_id__tc_id(ib_id_list):
        fragments = genesilencing_service.get_silencing_fragments(
                ib_id_list=ib_id_list)
        return {f['id']: f.get('geneIds') for f in fragments}

    step__ib_id__tc_id = Step(IB_ID, TC_ID,
            category=CAT_GENE_FUNCTION,
            convert_func=func__ib_id__tc_id,
            description='Get Tribolium genes silenced by the iB fragments')

#     def func__go_id__go_term(go_id_list):
#         terms = geneontology_service.get_go_terms(go_id_list)
#         return {t['id']: [t.get('name')] for t in terms}

#     step__go_id__go_term = Step(GO_ID, GO_TERM,
#             category=CAT_GENE_FUNCTION,
#             convert_func=func__go_id__go_term,
#             description='Convert GO IDs to theirs corresponding name')

#     def func__go_id__go_aspect(go_id_list):
#         terms = geneontology_service.get_go_terms(go_id_list)
#         return {t['id']: [t.get('aspect')] for t in terms}

#     step__go_id__go_aspect = Step(GO_ID, GO_ASPECT,
#             category=CAT_GENE_FUNCTION,
#             convert_func=func__go_id__go_aspect,
#             description='Convert GO IDs to one of the three GO aspects')

#     def func__gene_id__go_id(gene_id_list):
#         annotations = geneontology_service.get_annotations(gene_id_list=gene_id_list)
#         mapping = defaultdict(list)
#         for ann in annotations:
#             mapping[ann['geneId']].append(ann['term']['id'])
#         return mapping

#     step__tc_id__go_id = Step(TC_ID, GO_ID,
#             category=CAT_GENE_FUNCTION,
#             convert_func=func__gene_id__go_id,
#             description='Get GO ID for Tribolium genes')

#     step__dm_id__go_id = Step(DM_ID, GO_ID,
#             category=CAT_GENE_FUNCTION,
#             convert_func=func__gene_id__go_id,
#             description='Get GO ID for Drosophila genes')


#     def func__go_id__tc_id(go_id_list):
#         annotations = geneontology_service.get_annotations(go_id_list=go_id_list)
#         mapping = defaultdict(list)
#         tc_pat = re.compile('^TC[0-9]{6}$')
#         for ann in annotations:
#             gene_id = ann['geneId']
#             if tc_pat.match(gene_id):
#                 mapping[ann['term']['id']].append(gene_id)
#         return mapping

#     step__go_id__tc_id = Step(GO_ID, TC_ID,
#             category=CAT_GENE_FUNCTION,
#             convert_func=func__go_id__tc_id,
#             description='Get Tribolium genes for GO IDs')


#     def func__go_id__dm_id(go_id_list):
#         annotations = geneontology_service.get_annotations(go_id_list=go_id_list)
#         mapping = defaultdict(list)
#         dm_pat = re.compile('^FBgn[0-9]{7}$')
#         for ann in annotations:
#             gene_id = ann['geneId']
#             if dm_pat.match(gene_id):
#                 mapping[ann['term']['id']].append(gene_id)
#         return mapping

#     step__go_id__dm_id = Step(GO_ID, DM_ID,
#             category=CAT_GENE_FUNCTION,
#             convert_func=func__go_id__dm_id,
#             description='Get Drosophila genes for GO IDs')

    def func__ib_id__dali11(ib_id_list):
        mapping = {ib: phenotypeservice.get_lethality_values(ib).get('dali11')
                for ib in ib_id_list}
        mapping = {ib: [value] for ib, value in mapping.items()
                if value != -1}
        return mapping

    step__ib_id__dali11 = Step(IB_ID, LETHALITY_LARVAL_11,
            category=CAT_GENE_FUNCTION,
            convert_func=func__ib_id__dali11,
            description='Get lethality on day 11 in iBeetle larval screen')


    def func__ib_id__dali22(ib_id_list):
        mapping = {ib: phenotypeservice.get_lethality_values(ib).get('dali22')
                for ib in ib_id_list}
        mapping = {ib: [value] for ib, value in mapping.items()
                if value != -1}
        return mapping

    step__ib_id__dali22 = Step(IB_ID, LETHALITY_LARVAL_22,
            category=CAT_GENE_FUNCTION,
            convert_func=func__ib_id__dali22,
            description='Get lethality on day 22 in iBeetle larval screen')


    def func__ib_id__dapi11(ib_id_list):
        mapping = {ib: phenotypeservice.get_lethality_values(ib).get('dapi11')
                for ib in ib_id_list}
        mapping = {ib: [value] for ib, value in mapping.items()
                if value != -1}
        return mapping

    step__ib_id__dapi11 = Step(IB_ID, LETHALITY_PUPAL_11,
            category=CAT_GENE_FUNCTION,
            convert_func=func__ib_id__dapi11,
            description='Get lethality on day 11 in iBeetle pupal screen')


    return [
        step__dm_id__dm_symbol,
        step__dm_id__dm_name,
        step__dm_id__dm_cg,
        step__dm_symbol__dm_id,
        step__dm_cg__dm_id,
        step__dm_id__tc_id,
        step__tc_id__dm_id,
        step__tc_id__ib_id,
        step__ib_id__tc_id,
        # step__go_id__go_term,
        # step__go_id__go_aspect,
        # step__tc_id__go_id,
        # step__dm_id__go_id,
        # step__go_id__tc_id,
        # step__go_id__dm_id,
        step__ib_id__dali11,
        step__ib_id__dali22,
        step__ib_id__dapi11,
    ]
