const STORE_KEY='immuneerrorradar.workbench.history.v3075';
let researchIndex={receipts:[],manifestPreview:[],keyDocs:[],artifactHashes:[]};
let history=loadHistory();
let selectedId=null;

const $=id=>document.getElementById(id);
function nowIso(){return new Date().toISOString();}
function today(){return new Date().toISOString().slice(0,10);}
function loadHistory(){try{return JSON.parse(localStorage.getItem(STORE_KEY)||'[]')}catch{return []}}
function saveHistory(){localStorage.setItem(STORE_KEY,JSON.stringify(history));}
function outcomeFromText(t){const s=t.toUpperCase();
 if(s.includes('INVEST_IN_DATA_ONLY')) return 'DATA_ONLY_SURVIVED_FIRST_TRIAGE';
 if(s.includes('DO_NOT_INVEST_CLAIM_KILLED')||s.includes('CLAIM_KILLED')||s.includes('KILLED_')) return 'KILLED';
 if(s.includes('NOT_MEASURABLE')||s.includes('NOT TESTABLE')) return 'NOT_MEASURABLE';
 if(s.includes('WATCHLIST')) return 'WATCHLIST';
 if(s.includes('NULL')) return 'NULL_LIKE_OR_INCONCLUSIVE';
 if(s.includes('SURVIV')) return 'SURVIVED_LOCAL_DIRECTION_REVIEW_ONLY';
 return 'UNCLASSIFIED_REVIEW_ONLY';}
function titleFromText(t){const s=t.toUpperCase();
 const map=[['CSNK2A1','CK2/CSNK2A1 -> APM mechanism claim'],['CK2','CK2/CSNK2A1 -> APM mechanism claim'],['HDAC','HDAC/DNMT -> APM mechanism claim'],['DNMT','HDAC/DNMT -> APM mechanism claim'],['NECTIN2','NECTIN2/TIGIT bulk checkpoint claim'],['TIGIT','NECTIN2/TIGIT bulk checkpoint claim'],['GAMMA','gamma-delta/NKG2D surrogate claim'],['ΓΔ','gamma-delta/NKG2D surrogate claim'],['NKG2D','gamma-delta/NKG2D surrogate claim'],['ODC1','ODC1/polyamine axis'],['CD276','CD276/B7-H3 subgroup route'],['B7-H3','CD276/B7-H3 subgroup route'],['B2M','APM/B2M-TAP-HLA data axis'],['TAP1','APM/B2M-TAP-HLA data axis'],['HLA','APM/B2M-TAP-HLA data axis'],['APM','APM/B2M-TAP-HLA data axis']];
 let base='Hypothesis stress-test report'; for(const [k,v] of map){if(s.includes(k)){base=v;break}}
 const out=outcomeFromText(t); const suffix={KILLED:' — killed as written',DATA_ONLY_SURVIVED_FIRST_TRIAGE:' — data-only follow-up',NOT_MEASURABLE:' — not measurable',WATCHLIST:' — watchlist',NULL_LIKE_OR_INCONCLUSIVE:' — null-like/inconclusive',SURVIVED_LOCAL_DIRECTION_REVIEW_ONLY:' — review-only survivor'}[out]||' — review only';
 return base+suffix;}
function addReport(text, source='manual'){const created=nowIso(); const title=titleFromText(text); const outcome=outcomeFromText(text); const id='r_'+created.replace(/[-:.TZ]/g,'')+'_'+Math.random().toString(36).slice(2,8); history.unshift({id,created,date:created.slice(0,10),title,outcome,source,text}); saveHistory(); selectedId=id; renderAll(); $('statusLine').textContent=`Added: ${title}`; $('hypothesisInput').value='';}
function renderAll(){renderDates();renderReports();renderSelected();renderLedger();}
function renderDates(){const dates=[...new Set(history.map(r=>r.date))].sort().reverse(); const sel=$('dateSelect'); const old=sel.value; sel.innerHTML=''; if(!dates.length){sel.innerHTML='<option>No reports yet</option>';return} for(const d of dates){const o=document.createElement('option');o.value=d;o.textContent=`${d} (${history.filter(r=>r.date===d).length})`;sel.appendChild(o)} if(dates.includes(old))sel.value=old; else sel.value=history.find(r=>r.id===selectedId)?.date||dates[0];}
function renderReports(){const date=$('dateSelect').value; const list=history.filter(r=>r.date===date).sort((a,b)=>b.created.localeCompare(a.created)); const sel=$('reportSelect'); sel.innerHTML=''; for(const r of list){const o=document.createElement('option');o.value=r.id;o.textContent=`${r.created.slice(11,16)} · ${r.outcome} · ${r.title}`;sel.appendChild(o)} if(list.some(r=>r.id===selectedId)) sel.value=selectedId; else if(list[0]){selectedId=list[0].id;sel.value=selectedId;}}
function selected(){return history.find(r=>r.id===selectedId)}
function renderSelected(){const r=selected(); if(!r){$('reportTitle').textContent='Selected report';$('reportMeta').textContent='No report selected.';$('reportView').textContent='';return} $('reportTitle').textContent=r.title; $('reportMeta').textContent=`${r.created} · ${r.outcome} · source=${r.source}`; $('reportView').textContent=r.text;}
function renderLedger(){const counts={}; for(const r of history){counts[r.outcome]=(counts[r.outcome]||0)+1} $('ledgerStats').innerHTML=Object.entries(counts).map(([k,v])=>`<span class="stat">${k}: ${v}</span>`).join('')||'<span class="stat">No entries</span>'; const body=$('ledgerTable').querySelector('tbody'); body.innerHTML=''; for(const r of history.slice(0,100)){const tr=document.createElement('tr'); tr.innerHTML=`<td>${r.created.slice(0,10)}</td><td>${r.outcome}</td><td>${escapeHtml(r.title)}</td>`; body.appendChild(tr)}}
function escapeHtml(s){return String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]))}
function download(name, text, type='text/plain'){const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([text],{type}));a.download=name;document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove()},200)}
function csvEscape(x){return '"'+String(x).replace(/"/g,'""')+'"'}
function renderTab(tab='receipts'){document.querySelectorAll('.tabButtons button').forEach(b=>b.classList.toggle('active',b.dataset.tab===tab)); const c=$('tabContent');
 if(tab==='receipts'){c.innerHTML=`<h3>Receipts / Hashes</h3><p>${researchIndex.receipts?.length||0} indexed receipt entries. Local workbench receipts are unsigned unless stated otherwise.</p><pre>${escapeHtml(JSON.stringify(researchIndex.receipts||[],null,2).slice(0,12000))}</pre>`}
 if(tab==='manifest'){c.innerHTML=`<h3>Targeted GPL5175 review manifest</h3><p>${researchIndex.manifestRowCount||0} rows indexed. Preview only.</p><pre>${escapeHtml(JSON.stringify(researchIndex.manifestPreview||[],null,2).slice(0,16000))}</pre>`}
 if(tab==='tier0'){c.innerHTML='<h3>Tier-0 boundary</h3><p>Tier-0 proves replayability and claim discipline, not biology, diagnosis, treatment, clinical validity, or wet-lab efficacy.</p><ul><li>No clinical claim.</li><li>No wet-lab promotion.</li><li>No pan-pediatric claim from one cohort.</li><li>APM is data-only follow-up.</li></ul>'}
 if(tab==='replay'){c.innerHTML='<h3>Replay description</h3><p>Replay success means the same route, decision state, missing gates, and claim guard can be reconstructed from the repository artifacts. It does not certify biological truth.</p><ol><li>Verify receipts/hash index.</li><li>Verify targeted manifest.</li><li>Read Tier-0 boundaries.</li><li>Run static checks or Android harness if needed.</li></ol>'}
 if(tab==='apk'){c.innerHTML='<h3>APK integration bridge</h3><p>The APK is optional. It can be used as an Android runtime harness or integrated into another project by consuming reports/receipts as files. The GitHub workbench remains the primary researcher interface.</p><pre>Artifact name: ImmuneErrorRadar-debug-apk\nUse: optional runtime harness / report generator\nBoundary: not primary scholarly artifact</pre>'}
}
async function loadIndex(){try{const r=await fetch('data/research_index.json');researchIndex=await r.json();$('statusLine').textContent='Workbench index loaded.'}catch(e){$('statusLine').textContent='Index not loaded. Use a local server or upload files manually.'}renderTab('receipts')}
$('classifyBtn').onclick=()=>{const t=$('hypothesisInput').value.trim(); if(!t){$('statusLine').textContent='Paste a hypothesis or report first.';return} addReport(t)};
$('clearBtn').onclick=()=>{$('hypothesisInput').value='';$('statusLine').textContent='Input cleared.'};
$('fileInput').onchange=async e=>{for(const f of e.target.files){const text=await f.text(); addReport(text, f.name)} e.target.value=''};
$('dateSelect').onchange=()=>{selectedId=null;renderReports();renderSelected();};
$('reportSelect').onchange=e=>{selectedId=e.target.value;renderSelected();};
$('openReportBtn').onclick=renderSelected;
$('copyReportBtn').onclick=async()=>{const r=selected(); if(r){await navigator.clipboard.writeText(r.text);$('statusLine').textContent='Report copied.'}};
$('downloadReportBtn').onclick=()=>{const r=selected(); if(r) download(r.title.replace(/[^a-z0-9_-]+/gi,'_')+'.txt', r.text)};
$('printReportBtn').onclick=()=>window.print();
$('exportHistoryBtn').onclick=()=>download('immuneerrorradar_history.json', JSON.stringify(history,null,2),'application/json');
$('exportLedgerBtn').onclick=()=>download('immuneerrorradar_calibration_ledger.csv', ['date,outcome,title,source'].concat(history.map(r=>[r.created,r.outcome,r.title,r.source].map(csvEscape).join(','))).join('\n'),'text/csv');
document.querySelectorAll('.tabButtons button').forEach(b=>b.onclick=()=>renderTab(b.dataset.tab));
loadIndex(); renderAll();
