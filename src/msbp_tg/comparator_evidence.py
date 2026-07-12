
"""Step 19 comparator descriptor and journal-evidence hardening.

Compares pMSBP against existing descriptor columns in the open PolyMetriX
row-level table and tests whether pMSBP remains useful after comparator audit.
This is an audit step, not a journal claim.
"""
from __future__ import annotations
from pathlib import Path
import csv, math, random, statistics
from collections import defaultdict

POLYMETRIX_PATH = Path('data/open_row_level/LAMALAB_CURATED_Tg_structured_polymerclass.csv')
STEP18_FEATURE_PATH = Path('results/step18_open_data_pmsbp_reanalysis/polymetrix_open_pmsbp_feature_table.csv')

DESCRIPTOR_PATTERNS = {
    'num_rotatable_bonds': ['num_rotatable_bonds'],
    'num_rings': ['num_rings'],
    'num_aromatic_rings': ['num_aromatic_rings'],
    'molecular_weight': ['molecular_weight'],
    'heteroatom_density': ['heteroatom_density'],
    'topological_surface_area': ['topological_surface_area'],
    'num_hbond_acceptors': ['num_hbond_acceptors'],
    'num_hbond_donors': ['num_hbond_donors'],
}


def read_csv(path: Path):
    try:
        with path.open('r', newline='', encoding='utf-8') as f:
            return list(csv.DictReader(f))
    except UnicodeDecodeError:
        with path.open('r', newline='', encoding='latin-1') as f:
            return list(csv.DictReader(f))


def fnum(x):
    try:
        y = float(str(x).strip())
    except Exception:
        return None
    return None if math.isnan(y) or math.isinf(y) else y


def rank(vals):
    idx = sorted(enumerate(vals), key=lambda t: t[1])
    out = [0.0]*len(vals); i = 0
    while i < len(idx):
        j = i+1
        while j < len(idx) and idx[j][1] == idx[i][1]: j += 1
        av = (i+1+j)/2.0
        for k in range(i,j): out[idx[k][0]] = av
        i = j
    return out


def pearson(xs, ys):
    if len(xs) < 3 or len(xs) != len(ys): return None
    mx, my = statistics.fmean(xs), statistics.fmean(ys)
    vx = sum((x-mx)**2 for x in xs); vy = sum((y-my)**2 for y in ys)
    if vx <= 0 or vy <= 0: return None
    return sum((x-mx)*(y-my) for x,y in zip(xs,ys)) / math.sqrt(vx*vy)


def spearman(xs, ys):
    if len(xs) < 3 or len(xs) != len(ys): return None
    return pearson(rank(xs), rank(ys))


def qtile(vals, q):
    vals = sorted(v for v in vals if v is not None and not math.isnan(v))
    if not vals: return None
    if len(vals) == 1: return vals[0]
    pos = (len(vals)-1)*q; lo = math.floor(pos); hi = math.ceil(pos)
    if lo == hi: return vals[lo]
    return vals[lo]*(hi-pos) + vals[hi]*(pos-lo)


def ci(vals): return qtile(vals, 0.025), qtile(vals, 0.975)


def choose_columns(fields):
    chosen = {}
    lows = {f.lower(): f for f in fields}
    for name, pats in DESCRIPTOR_PATTERNS.items():
        matches = []
        for low, orig in lows.items():
            if any(p in low for p in pats): matches.append(orig)
        if matches:
            matches.sort(key=lambda m: (0 if 'fullpolymerlevel' in m.lower() and '_sum_' in m.lower() else 1, len(m), m))
            chosen[name] = matches[0]
    return chosen


def load_rows(root: Path):
    raw = read_csv(root/POLYMETRIX_PATH)
    feat = read_csv(root/STEP18_FEATURE_PATH)
    cols = choose_columns(list(raw[0].keys()) if raw else [])
    rows = []
    for fr in feat:
        idx = int(fr['row_index'])
        rr = raw[idx]
        tg = fnum(fr.get('Exp_Tg_K')); pm = fnum(fr.get('pmsbp_density'))
        if tg is None or pm is None: continue
        row = {'row_index': idx, 'Exp_Tg_K': tg, 'pmsbp_density': pm,
               'polymer_class': fr.get('polymer_class') or rr.get('meta.polymer_class') or 'unknown_class',
               'source': fr.get('source') or rr.get('meta.source') or 'unknown_source'}
        for name,col in cols.items(): row[name] = fnum(rr.get(col))
        rot = row.get('num_rotatable_bonds'); mw = row.get('molecular_weight')
        if isinstance(rot,float) and isinstance(mw,float) and mw != 0:
            row['rotatable_per_mw'] = rot/mw
            row['negative_rotatable_per_mw'] = -rot/mw
        rows.append(row)
    if any('rotatable_per_mw' in r for r in rows):
        cols['rotatable_per_mw'] = 'derived:num_rotatable_bonds/molecular_weight'
        cols['negative_rotatable_per_mw'] = 'derived:-num_rotatable_bonds/molecular_weight'
    return rows, cols


def valid_xy(rows, xname, yname='Exp_Tg_K'):
    xs=[]; ys=[]; kept=[]
    for r in rows:
        x = r.get(xname); y = r.get(yname)
        if isinstance(x,float) and isinstance(y,float) and not any(math.isnan(v) or math.isinf(v) for v in [x,y]):
            xs.append(x); ys.append(y); kept.append(r)
    return xs,ys,kept


def residual_pairs(rows, xname):
    groups=defaultdict(list)
    for r in rows:
        if isinstance(r.get(xname),float) and isinstance(r.get('Exp_Tg_K'),float):
            groups[str(r.get('polymer_class','unknown'))].append(r)
    xs=[]; ys=[]
    for gr in groups.values():
        xv=[r[xname] for r in gr]; yv=[r['Exp_Tg_K'] for r in gr]
        cx=statistics.median(xv); cy=statistics.median(yv)
        for r in gr:
            xs.append(r[xname]-cx); ys.append(r['Exp_Tg_K']-cy)
    return xs,ys


def association(rows, names):
    out=[]
    for n in names:
        xs,ys,kept=valid_xy(rows,n)
        rx,ry=residual_pairs(kept,n)
        raw=spearman(xs,ys); res=spearman(rx,ry)
        out.append({'descriptor':n,'n_rows':len(kept),'n_polymer_classes':len({r.get('polymer_class') for r in kept}),
                    'raw_spearman_rho':raw,'within_class_median_residual_spearman_rho':res,
                    'abs_within_class_residual_rho':abs(res or 0.0)})
    out.sort(key=lambda r:(-float(r['abs_within_class_residual_rho']), str(r['descriptor'])))
    return out


def cluster_boot(rows, names, n_boot=200, seed=19019):
    rng=random.Random(seed); groups=defaultdict(list)
    for r in rows: groups[str(r.get('polymer_class','unknown'))].append(r)
    keys=list(groups)
    out=[]
    for n in names:
        vals=[]
        for _ in range(n_boot):
            sample=[]
            for _j in range(len(keys)): sample.extend(groups[keys[rng.randrange(len(keys))]])
            xs,ys=residual_pairs(sample,n); rho=spearman(xs,ys)
            if rho is not None: vals.append(rho)
        lo,hi=ci(vals)
        out.append({'descriptor':n,'bootstrap_type':'polymer_class_cluster_bootstrap','n_bootstrap':n_boot,
                    'within_class_residual_rho_ci_low':lo,'within_class_residual_rho_ci_high':hi,
                    'n_valid_bootstrap':len(vals)})
    return out


def solve(a,b):
    n=len(b); m=[row[:] + [rhs] for row,rhs in zip(a,b)]
    for c in range(n):
        p=max(range(c,n), key=lambda r: abs(m[r][c]))
        if abs(m[p][c]) < 1e-12: return None
        if p != c: m[c],m[p] = m[p],m[c]
        div=m[c][c]
        for j in range(c,n+1): m[c][j] /= div
        for r in range(n):
            if r == c: continue
            fac=m[r][c]
            for j in range(c,n+1): m[r][j] -= fac*m[c][j]
    return [m[i][n] for i in range(n)]


def linear_r2(rows, feats, yname='tg_resid'):
    data=[]; y=[]
    for r in rows:
        vals=[]; ok=True
        for f in feats:
            v=r.get(f)
            if not isinstance(v,float): ok=False; break
            vals.append(v)
        yy=r.get(yname)
        if ok and isinstance(yy,float): data.append([1.0]+vals); y.append(yy)
    n=len(y); p=len(feats)+1
    if n <= p+2: return None,n
    cols=list(zip(*data)); means=[0.0]; sds=[1.0]
    for col in cols[1:]:
        mu=statistics.fmean(col); var=sum((v-mu)**2 for v in col)/len(col); sd=math.sqrt(var) if var>0 else 1.0
        means.append(mu); sds.append(sd)
    sx=[]
    for row in data: sx.append([1.0]+[(row[j]-means[j])/sds[j] for j in range(1,p)])
    xtx=[[0.0]*p for _ in range(p)]; xty=[0.0]*p
    for row,yy in zip(sx,y):
        for i in range(p):
            xty[i]+=row[i]*yy
            for j in range(p): xtx[i][j]+=row[i]*row[j]
    for i in range(p): xtx[i][i]+=1e-8
    beta=solve(xtx,xty)
    if beta is None: return None,n
    ybar=statistics.fmean(y); sst=sum((yy-ybar)**2 for yy in y)
    if sst <= 0: return None,n
    ssr=sum((yy-sum(b*x for b,x in zip(beta,row)))**2 for row,yy in zip(sx,y))
    return 1-ssr/sst,n


def with_residual_columns(rows, names):
    groups=defaultdict(list)
    for r in rows: groups[str(r.get('polymer_class','unknown'))].append(r)
    out=[]
    for gr in groups.values():
        tgs=[r['Exp_Tg_K'] for r in gr if isinstance(r.get('Exp_Tg_K'),float)]
        if not tgs: continue
        tc=statistics.median(tgs); centers={}
        for n in names:
            vals=[r[n] for r in gr if isinstance(r.get(n),float)]
            if vals: centers[n]=statistics.median(vals)
        for r in gr:
            rr=dict(r); rr['tg_resid']=r['Exp_Tg_K']-tc
            for n,c in centers.items():
                if isinstance(r.get(n),float): rr[n+'_resid']=r[n]-c
            out.append(rr)
    return out


def incremental(rows,names):
    comps=[n for n in names if n!='pmsbp_density']
    pref=['num_rotatable_bonds','rotatable_per_mw','num_rings','num_aromatic_rings','molecular_weight','heteroatom_density']
    base=[d for d in pref if d in comps] or comps[:5]
    resid=with_residual_columns(rows, list(dict.fromkeys(base+['pmsbp_density'])))
    bf=[d+'_resid' for d in base]; pf=['pmsbp_density_resid']; plus=bf+pf
    p_r2,p_n=linear_r2(resid,pf); b_r2,b_n=linear_r2(resid,bf); plus_r2,plus_n=linear_r2(resid,plus)
    delta = plus_r2-b_r2 if isinstance(plus_r2,float) and isinstance(b_r2,float) else None
    return [
      {'model':'pmsbp_only_within_class_residual_linear','features':';'.join(pf),'n_rows_complete_case':p_n,'r2':p_r2,'delta_r2_vs_base':''},
      {'model':'base_comparators_within_class_residual_linear','features':';'.join(bf),'n_rows_complete_case':b_n,'r2':b_r2,'delta_r2_vs_base':''},
      {'model':'base_plus_pmsbp_within_class_residual_linear','features':';'.join(plus),'n_rows_complete_case':plus_n,'r2':plus_r2,'delta_r2_vs_base':delta},
    ]


def redundancy(rows,names):
    out=[]
    for n in names:
        if n=='pmsbp_density': continue
        xs,ys,kept=valid_xy(rows,'pmsbp_density',n)
        rho=spearman(xs,ys)
        out.append({'comparator':n,'n_rows':len(kept),'spearman_rho_with_pmsbp':rho,'abs_spearman_with_pmsbp':abs(rho or 0.0)})
    out.sort(key=lambda r:(-float(r['abs_spearman_with_pmsbp']), str(r['comparator'])))
    return out


def verdict(assoc,incr,red):
    p=next((r for r in assoc if r['descriptor']=='pmsbp_density'),{})
    plus=next((r for r in incr if r['model']=='base_plus_pmsbp_within_class_residual_linear'),{})
    pabs=float(p.get('abs_within_class_residual_rho') or 0.0)
    delta=plus.get('delta_r2_vs_base')
    maxred=max([float(r.get('abs_spearman_with_pmsbp') or 0.0) for r in red] or [0.0])
    if pabs >= 0.20 and isinstance(delta,float) and delta >= 0.005:
        return 'STEP19_GO_INCREMENTAL_DESCRIPTOR_EVIDENCE_SUPPORTED'
    if pabs >= 0.20 and maxred < 0.98:
        return 'STEP19_REVISE_AS_OPEN_DATA_DESCRIPTOR_OBSERVATION_NOT_INCREMENTAL_LOCKED'
    if maxred >= 0.98:
        return 'STEP19_REPOSITION_AS_ROTATABLE_MOBILITY_DESCRIPTOR_NOT_NEW_PRINCIPLE'
    return 'STEP19_NO_GO_COMPARATOR_EVIDENCE_WEAK'


def write_csv(path, rows, fields=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    fields=fields or (list(rows[0]) if rows else [])
    with path.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)


def write_step19_outputs(root: Path, output_dir: Path, n_bootstrap: int = 200, seed: int = 19019):
    output_dir.mkdir(parents=True, exist_ok=True)
    rows, cols = load_rows(root)
    names=['pmsbp_density'] + [d for d in cols]
    coverage=[]
    for n in names:
        cnt=sum(1 for r in rows if isinstance(r.get(n),float))
        coverage.append({'descriptor':n,'source_column':'derived:step18_pmsbp_feature_table' if n=='pmsbp_density' else cols.get(n,''),
                         'n_rows_available':cnt,'fraction_available':cnt/len(rows) if rows else 0.0})
    assoc=association(rows,names); boot=cluster_boot(rows,names,n_bootstrap,seed); incr=incremental(rows,names); red=redundancy(rows,names)
    v=verdict(assoc,incr,red)
    write_csv(output_dir/'descriptor_coverage_summary.csv', coverage)
    write_csv(output_dir/'descriptor_univariate_association_summary.csv', assoc)
    write_csv(output_dir/'descriptor_cluster_bootstrap_ci.csv', boot)
    write_csv(output_dir/'incremental_residual_linear_model_summary.csv', incr)
    write_csv(output_dir/'pmsbp_redundancy_vs_comparators.csv', red)
    write_csv(output_dir/'step19_journal_evidence_hardening_verdict.csv', [{'verdict':v}])
    p=next((r for r in assoc if r['descriptor']=='pmsbp_density'),{})
    lines=['# Step 19 - Comparator Descriptor Evidence Hardening','',f'Verdict: `{v}`','',
           '## pMSBP','',f"- raw rho: {p.get('raw_spearman_rho')}",f"- within-class residual rho: {p.get('within_class_median_residual_spearman_rho')}",'',
           '## Top descriptor associations','']
    for r in assoc[:8]: lines.append(f"- {r['descriptor']}: residual rho={r.get('within_class_median_residual_spearman_rho')}, n={r.get('n_rows')}")
    lines += ['', '## Incremental model audit', '']
    for r in incr: lines.append(f"- {r['model']}: R2={r.get('r2')}, delta={r.get('delta_r2_vs_base')}, n={r.get('n_rows_complete_case')}")
    lines += ['', '## Redundancy audit', '']
    for r in red[:8]: lines.append(f"- pMSBP vs {r['comparator']}: rho={r.get('spearman_rho_with_pmsbp')}, n={r.get('n_rows')}")
    lines += ['', '## Interpretation', '', 'This audit decides whether the manuscript should be framed as an incremental descriptor result, a limited open-data observation, or a repositioned rotatable-mobility study.']
    (output_dir/'STEP19_COMPARATOR_DESCRIPTOR_EVIDENCE_HARDENING_REPORT.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    return v
