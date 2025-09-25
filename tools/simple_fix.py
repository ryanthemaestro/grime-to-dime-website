#!/usr/bin/env python3
"""
Simple fix for the landing page generator
"""

from pathlib import Path

def main():
    path = Path('tools/generate_landing_pages.py')
    text = path.read_text()
    
    # Simple approach: just replace __FORM_SCRIPT__ directly in render function
    old_line = "    return html_output.replace(\"__FORM_SCRIPT__\", form_script)"
    
    new_lines = '''    # Simple form script injection without complex formatting
    simple_form_script = """
    <script>
        function getQueryParam(n){var p=new URLSearchParams(window.location.search);var v=p.get(n);return v&&v.trim()?v.trim():''}
        function setCookie(n,v,a){if(!n)return;var parts=[n+'='+encodeURIComponent(v||'')];parts.push('path=/');if(a)parts.push('max-age='+a);parts.push('samesite=Lax');if(location.protocol==='https:')parts.push('secure');document.cookie=parts.join('; ')}
        function getCookie(n){var m=document.cookie.match(new RegExp('(?:^|; )'+n.replace(/([.$?*|{}()\\\\[\\\\]\\\\\\\\\\\\+^])/g,'\\\\\\\\$1')+'=([^;]*)'));return m?decodeURIComponent(m[1]):''}
        function storeGclidFromUrl(){var g=getQueryParam('gclid');if(!g)return;try{localStorage.setItem('gclid',g);}catch(e){} setCookie('gclid',g,60*60*24*90)}
        function getStoredGclid(){try{var ls=localStorage.getItem('gclid');if(ls)return ls;}catch(e){} return getCookie('gclid')||''}
        function ensureGclidInput(f){if(!f)return;var el=f.querySelector('input[name="gclid"]');if(!el){el=document.createElement('input');el.type='hidden';el.name='gclid';f.appendChild(el)}var v=getStoredGclid();if(v)el.value=v}
        document.addEventListener('DOMContentLoaded',function(){try{storeGclidFromUrl();}catch(e){} var f=document.getElementById('quoteForm'); if(f) try{ensureGclidInput(f);}catch(e){}});
        function handleFormSubmit(ev){ev.preventDefault();var name=document.getElementById('name').value;var phone=document.getElementById('phone').value;var email=document.getElementById('email').value; if(!name||!phone){alert('Please provide your name and phone.');return false} var er=/^[^\\\\s@]+@[^\\\\s@]+\\\\.[^\\\\s@]+$/; if(email && !er.test(email)){alert('Please enter a valid email.');return false} var pr=/(\\\\+?1[-. ]?)?\\\\(?([0-9]{3})\\\\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/; if(!pr.test(phone)){alert('Please enter a valid phone.');return false}
            var form=document.getElementById('quoteForm'); try{ensureGclidInput(form);}catch(e){} var btn=document.querySelector('.submit-button'); var t=btn.innerHTML; btn.innerHTML='<i class="fas fa-spinner fa-spin"></i> Processing...'; btn.disabled=true; var fd=new FormData(form); fetch(form.action,{method:'POST',body:fd,headers:{'Accept':'application/json'}}).then(function(r){ if(r.ok){ if(typeof gtag!=='undefined'){ gtag('event','generate_lead'); gtag('event','form_submission',{ 'event_category':'Quote','event_label':'""" + html.escape(group.get("name", "Landing Page")) + """' }); gtag('event','conversion',{ 'send_to':'AW-11553122519/0KjoCPG_6oQbENfR-oQr','value':1.0,'transaction_id':'lead_'+Date.now().toString() }); } window.location.href=form.getAttribute('_next')||'/thank-you.html'; } else { throw new Error('Network response was not ok'); }}).catch(function(e){ console.error('Error:',e); btn.innerHTML=t; btn.disabled=false; alert('There was a problem submitting your form. Please try again.');}); return false; }
    </script>
    """
    
    return html_output.replace("__FORM_SCRIPT__", simple_form_script)'''
    
    if old_line in text:
        text = text.replace(old_line, new_lines)
        
        # Remove the old form script handling
        old_form_stuff = """    # Handle form script injection
    form_event_label = html.escape(group.get("name", "Landing Page"))
    form_script = FORM_SCRIPT.format(form_event_label=form_event_label)
    
    html_output = HTML_TEMPLATE.format("""
        
        text = text.replace(old_form_stuff, "    html_output = HTML_TEMPLATE.format(")
        
        path.write_text(text)
        print("✅ Fixed!")
    else:
        print("❌ Could not find target line")

if __name__ == "__main__":
    main()
