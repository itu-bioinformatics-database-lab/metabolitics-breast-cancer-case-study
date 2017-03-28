from .cli import cli
from services import NamingService, DataReader


def report_matching(a, b, a_name, b_name):
    print('%s matching %s:' % (a_name, b_name), a.intersection(b))
    print('%s matching %s len:' % (a_name, b_name), len(a.intersection(b)))
    print('total:', len(a))
    print()


@cli.command()
def naming_issue():

    human_names = set(NamingService('recon')._names.keys())

    dr = DataReader()
    bc_names = set(i.lower().strip() for i in dr.read_columns('BC'))
    hcc_names = set(i.lower().strip() for i in dr.read_columns('HCC'))

    report_matching(hcc_names, bc_names, 'hcc', 'bc')

    print('-' * 10, 'human', '-' * 10)
    report_matching(hcc_names, human_names, 'hcc', '')
    report_matching(bc_names, human_names, 'bc', '')
