from pathlib import Path
import csv
from msbp_tg.comparator_evidence import spearman, linear_r2, write_step19_outputs


def test_spearman_negative():
    assert spearman([1,2,3],[3,2,1]) == -1.0


def test_linear_r2_simple():
    rows=[{'y':1.0,'x':1.0},{'y':2.0,'x':2.0},{'y':3.0,'x':3.0},{'y':4.0,'x':4.0}]
    r2,n=linear_r2(rows,['x'], yname='y')
    assert n == 4
    assert r2 is not None and r2 > 0.99


def test_step19_synthetic(tmp_path: Path):
    d=tmp_path/'data/open_row_level'; d.mkdir(parents=True)
    raw=d/'LAMALAB_CURATED_Tg_structured_polymerclass.csv'
    fields=['labels.Exp_Tg(K)','meta.polymer_class','meta.source','fullpolymerlevel.features.num_rotatable_bonds_sum_fullpolymerfeaturizer','fullpolymerlevel.features.num_rings_sum_fullpolymerfeaturizer','fullpolymerlevel.features.molecular_weight_sum_fullpolymerfeaturizer','fullpolymerlevel.features.heteroatom_density_sum_fullpolymerfeaturizer']
    with raw.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=fields); w.writeheader()
        for i in range(10):
            cls='A' if i<5 else 'B'; j=i%5
            w.writerow({'labels.Exp_Tg(K)':str(300+10*j+(100 if cls=='B' else 0)), 'meta.polymer_class':cls, 'meta.source':'demo', 'fullpolymerlevel.features.num_rotatable_bonds_sum_fullpolymerfeaturizer':str(5-j), 'fullpolymerlevel.features.num_rings_sum_fullpolymerfeaturizer':str(j%2), 'fullpolymerlevel.features.molecular_weight_sum_fullpolymerfeaturizer':str(100+j), 'fullpolymerlevel.features.heteroatom_density_sum_fullpolymerfeaturizer':str(0.1*j)})
    s18=tmp_path/'results/step18_open_data_pmsbp_reanalysis'; s18.mkdir(parents=True)
    fp=s18/'polymetrix_open_pmsbp_feature_table.csv'
    fields=['row_index','Exp_Tg_K','pmsbp_density','representation_class','polymer_class','source','reliability','PSMILES']
    with fp.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=fields); w.writeheader()
        for i in range(10):
            cls='A' if i<5 else 'B'; j=i%5
            w.writerow({'row_index':i,'Exp_Tg_K':str(300+10*j+(100 if cls=='B' else 0)),'pmsbp_density':str(-0.5-0.05*j),'representation_class':'*demo*','polymer_class':cls,'source':'demo','reliability':'black','PSMILES':'[*]CC[*]'})
    v=write_step19_outputs(tmp_path, tmp_path/'results/step19', n_bootstrap=20)
    assert v.startswith('STEP19_')
    assert (tmp_path/'results/step19/descriptor_univariate_association_summary.csv').exists()
