import React, {useEffect, useState} from "react";
import {createRoot} from "react-dom/client";
import "./style.css";

const API="http://localhost:8000/api";

function Card({title,value}){return <div className="card"><div className="muted">{title}</div><div className="metric">{value}</div></div>}

function App(){
 const [dash,setDash]=useState({});
 const [properties,setProperties]=useState([]);
 const [investors,setInvestors]=useState([]);
 const [matches,setMatches]=useState([]);
 const [tab,setTab]=useState("Dashboard");
 const [busy,setBusy]=useState(false);

 async function load(){
   const [d,p,i,m]=await Promise.all([
     fetch(API+"/dashboard").then(x=>x.json()),
     fetch(API+"/properties").then(x=>x.json()),
     fetch(API+"/investors").then(x=>x.json()),
     fetch(API+"/matches").then(x=>x.json())
   ]);
   setDash(d); setProperties(p); setInvestors(i); setMatches(m);
 }
 useEffect(()=>{load()},[]);

 async function generate(){
   setBusy(true);
   await fetch(API+"/matches/generate",{method:"POST"});
   await load(); setBusy(false); alert("Matching completed.");
 }

 const nav=["Dashboard","Properties","Investors","Matches","Deals"];
 return <div className="app">
   <aside>
    <h1>Astra RE</h1><div className="subtitle">Real Estate Intelligence</div>
    {nav.map(n=><button className={tab===n?"active":""} onClick={()=>setTab(n)} key={n}>{n}</button>)}
    <div className="side-note">Local-first CRM<br/>Source-aware data<br/>Human approval workflow</div>
   </aside>
   <main>
    <header><div><h2>{tab}</h2><span className="muted">Lead → Match → Deal → Revenue</span></div>
      <button className="primary" onClick={generate} disabled={busy}>{busy?"Matching…":"Generate Matches"}</button>
    </header>

    {tab==="Dashboard" && <section>
      <div className="grid">
       <Card title="Properties" value={dash.properties||0}/><Card title="Investors" value={dash.investors||0}/>
       <Card title="Matches" value={dash.matches||0}/><Card title="Deals" value={dash.deals||0}/>
       <Card title="Potential Commission" value={"$"+Number(dash.potential_commission||0).toLocaleString()}/>
       <Card title="Received Commission" value={"$"+Number(dash.received_commission||0).toLocaleString()}/>
      </div>
      <div className="panel"><h3>Workflow</h3><div className="flow">{["Discover","Verify","Analyze","Match","Human Review","Introduce","Deal","Close","Commission"].map((x,i)=><div key={x} className="step"><b>{i+1}</b>{x}</div>)}</div></div>
      <div className="panel"><h3>Safety & Data Integrity</h3><p>Connectors are designed for authorized APIs, licensed/public data and user-provided imports. No CAPTCHA bypassing, private-data harvesting, fake identities or deceptive outreach is built into this MVP.</p></div>
    </section>}

    {tab==="Properties" && <section className="panel"><h3>Properties ({properties.length})</h3><table><thead><tr><th>Address</th><th>Location</th><th>Type</th><th>Price</th><th>Source</th><th>Verification</th></tr></thead><tbody>{properties.map(p=><tr key={p.id}><td>{p.address}</td><td>{p.city}, {p.state}</td><td>{p.property_type}</td><td>{p.asking_price?`$${Number(p.asking_price).toLocaleString()}`:"—"}</td><td>{p.source}</td><td><span className="badge">{p.verification_status}</span></td></tr>)}</tbody></table></section>}

    {tab==="Investors" && <section className="panel"><h3>Investors ({investors.length})</h3><table><thead><tr><th>Name</th><th>Company</th><th>Location</th><th>Budget</th><th>Strategy</th><th>Cash</th></tr></thead><tbody>{investors.map(i=><tr key={i.id}><td>{i.name}</td><td>{i.company||"—"}</td><td>{i.location||"—"}</td><td>{i.min_price||i.max_price?`$${Number(i.min_price||0).toLocaleString()}–$${Number(i.max_price||0).toLocaleString()}`:"—"}</td><td>{i.strategies||"—"}</td><td>{i.cash_buyer?"Yes":"No"}</td></tr>)}</tbody></table></section>}

    {tab==="Matches" && <section className="panel"><h3>Investor Matches</h3>{matches.length===0?<p className="muted">No matches yet. Add/import properties and investors, then generate matches.</p>:<table><thead><tr><th>Property ID</th><th>Investor ID</th><th>Score</th><th>Reasons</th><th>Concerns</th></tr></thead><tbody>{matches.map(m=><tr key={m.id}><td>{m.property_id}</td><td>{m.investor_id}</td><td><strong>{m.score.toFixed(0)}</strong></td><td>{m.reasons||"—"}</td><td>{m.concerns||"—"}</td></tr>)}</tbody></table>}</section>}

    {tab==="Deals" && <section className="panel"><h3>Deal Management</h3><p>Deal API is ready at <code>/api/deals</code>. The next UI layer can add deal creation, contract milestones, commission approval and payment-provider webhooks.</p></section>}
   </main>
 </div>
}
createRoot(document.getElementById("root")).render(<App/>);
