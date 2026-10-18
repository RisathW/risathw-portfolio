(function(){
  /* loading screen: every page load, plus when leaving for another page */
  var ldr=document.getElementById('loader'),de=document.documentElement;
  if(ldr){
    var bar=ldr.querySelector('i'),pct=document.getElementById('pct'),n=0,ready=document.readyState==='complete',t0=Date.now(),tick;
    var fin=function(){ldr.classList.add('done');setTimeout(function(){if(ldr.classList.contains('done'))de.classList.remove('ld')},650)};
    var run=function(){
      clearInterval(tick);n=0;t0=Date.now();ldr.classList.remove('done');
      tick=setInterval(function(){
        n=Math.min(ready?100:90,n+(ready?9:3+Math.random()*3));
        bar.style.width=n+'%';pct.textContent=Math.round(n);
        if(n>=100&&Date.now()-t0>650){clearInterval(tick);setTimeout(fin,120)}
      },40);
    };
    if(de.classList.contains('ld')){
      addEventListener('load',function(){ready=true});
      setTimeout(function(){ready=true},3000);
      run();
    }else ldr.classList.add('done');
    /* coming back with the browser Back button (cached page) */
    addEventListener('pageshow',function(e){if(e.persisted){de.classList.remove('ld');ldr.classList.add('done');ldr.style.display=''}});
    /* show it again when moving to another page of the site */
    document.addEventListener('click',function(e){
      var a=e.target.closest&&e.target.closest('a[href]');
      if(!a||e.defaultPrevented||e.button||e.metaKey||e.ctrlKey||e.shiftKey||a.target==='_blank'||a.hasAttribute('download'))return;
      var u=new URL(a.href,location.href);
      if(u.origin!==location.origin||(u.pathname===location.pathname&&u.search===location.search))return;
      clearInterval(tick);ldr.style.display='';de.classList.add('ld');ldr.classList.remove('done');bar.style.width='25%';pct.textContent='25';
    });
  }

  var $=function(s,c){return (c||document).querySelector(s)},$$=function(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s))};

  /* nav */
  var nav=$('.nav'),burger=$('#burger'),menu=$('#menu');
  if(nav)addEventListener('scroll',function(){nav.classList.toggle('stuck',scrollY>10)},{passive:true});
  if(burger)burger.addEventListener('click',function(){var o=menu.classList.toggle('open');burger.classList.toggle('open',o);burger.setAttribute('aria-expanded',o)});
  $$('#menu a').forEach(function(a){a.addEventListener('click',function(){menu.classList.remove('open');burger&&burger.classList.remove('open')})});

  /* active link on scroll */
  var links=$$('#menu a[href^="#"]');
  if(links.length&&'IntersectionObserver' in window){
    var map={};links.forEach(function(a){map[a.getAttribute('href').slice(1)]=a});
    var so=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){links.forEach(function(l){l.classList.remove('on')});var l=map[e.target.id];l&&l.classList.add('on')}})},{rootMargin:'-45% 0px -50% 0px'});
    Object.keys(map).forEach(function(id){var s=document.getElementById(id);s&&so.observe(s)});
  }

  /* reveal */
  var rv=$$('.rv');
  if('IntersectionObserver' in window){
    var ro=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');ro.unobserve(e.target)}})},{threshold:.12});
    rv.forEach(function(el){ro.observe(el)});
  }else rv.forEach(function(el){el.classList.add('in')});

  /* portfolio tabs */
  var tabs=$$('.tabs button');
  tabs.forEach(function(b){b.addEventListener('click',function(){
    tabs.forEach(function(x){x.classList.toggle('on',x===b)});
    $$('.pane').forEach(function(p){p.classList.toggle('on',p.id===b.dataset.t)});
  })});

  /* software showcase */
  var shows=[
    {tag:'Digital infrastructure',text:'Fortechz: architecting elite digital infrastructure, from software development to IT infrastructure management.',link:'https://fortechz.com/',label:'Visit Fortechz',img:'assets/screenshots/fortechz.jpg'},
    {tag:'Website',text:'Sakura Pre-School: a bright, friendly preschool website, live on Vercel.',link:'https://sakura-pre-school.vercel.app/',label:'Visit Sakura',img:'assets/screenshots/sakura.jpg'},
    {tag:'Design studio',text:'ArtifeX Visual Studio: the portfolio site of the design studio I freelance with.',link:'https://risathw.github.io/artifex.github.io/',label:'Visit ArtifeX',img:'assets/screenshots/artifex.jpg'}
  ];
  var tb=$$('#thumbs button');
  tb.forEach(function(b){b.addEventListener('click',function(){
    var d=shows[b.dataset.i];tb.forEach(function(x){x.classList.toggle('on',x===b)});
    $('#s-tag').textContent=d.tag;$('#s-text').textContent=d.text;
    var l=$('#s-link');l.href=d.link;l.firstChild.textContent=d.label+' ';
    var i=$('#s-img');i.src=d.img;
  })});

  /* photo filters */
  $$('.filters button').forEach(function(b){b.addEventListener('click',function(){
    $$('.filters button').forEach(function(x){x.classList.toggle('on',x===b)});
    $$('.pgrid figure').forEach(function(f){f.classList.toggle('hide',b.dataset.f!=='all'&&f.dataset.cat!==b.dataset.f)});
  })});

  /* lightbox */
  var lb=$('#lb');
  if(lb){
    var li=$('img',lb);
    var close=function(){lb.classList.remove('on');lb.setAttribute('aria-hidden','true')};
    document.addEventListener('click',function(e){
      var f=e.target.closest&&e.target.closest('[data-full]');
      if(f){li.src=f.dataset.full;lb.classList.add('on');lb.setAttribute('aria-hidden','false')}
      else if(e.target===lb||e.target.closest('.lb button'))close();
    });
    addEventListener('keydown',function(e){if(e.key==='Escape')close()});
  }

  /* contact form (FormSubmit ajax) */
  var cf=$('#cform');
  if(cf){cf.addEventListener('submit',function(e){
    e.preventDefault();var m=$('#fmsg'),b=$('button',cf);
    m.className='fmsg';m.textContent='Sending...';b.disabled=true;
    fetch(cf.action,{method:'POST',headers:{'Accept':'application/json'},body:new FormData(cf)})
      .then(function(r){return r.json()})
      .then(function(d){
        if(d.success==='true'||d.success===true){cf.reset();m.className='fmsg ok';m.textContent='Thanks! Your message was sent. I will reply soon.'}
        else throw new Error(d.message||'Message was not accepted.');
      })
      .catch(function(err){
        var why=location.protocol==='file:'?'Open the site from its web address (not a local file) for the form to work.':(err&&err.message&&err.message!=='Failed to fetch'?err.message:'');
        m.className='fmsg err';m.textContent='Could not send. '+(why?why+' ':'')+'Please email me directly at risathwijethunga@gmail.com.'})
      .then(function(){b.disabled=false});
  })}

  /* share links on story page */
  var x=$('#share-x'),inn=$('#share-in');
  if(x){var u=encodeURIComponent(location.href),t=encodeURIComponent(document.title);
    x.href='https://twitter.com/intent/tweet?url='+u+'&text='+t;
    inn.href='https://www.linkedin.com/sharing/share-offsite/?url='+u}
})();
