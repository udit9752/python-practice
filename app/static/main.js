const form = document.getElementById('optForm');
const statusEl = document.getElementById('status');
const resultEl = document.getElementById('result');
const submitBtn = document.getElementById('submitBtn');

function setStatus(msg){
	statusEl.textContent = msg;
	statusEl.hidden = !msg;
}

function setLoading(loading){
	submitBtn.disabled = loading;
	submitBtn.textContent = loading ? 'Optimizing…' : 'Optimize';
}

form.addEventListener('submit', async (e) => {
	e.preventDefault();
	resultEl.hidden = true;
	resultEl.textContent = '';
	setStatus('Uploading and optimizing…');
	setLoading(true);

	try{
		const fd = new FormData(form);
		const format = fd.get('output_format') || 'text';

		const resp = await fetch('/optimize', { method: 'POST', body: fd });
		if(!resp.ok){
			let detail = '';
			try{ const j = await resp.json(); detail = j.detail || JSON.stringify(j); }catch{}
			throw new Error(`Error ${resp.status}: ${detail || resp.statusText}`);
		}

		if(format === 'docx'){
			const blob = await resp.blob();
			const url = URL.createObjectURL(blob);
			const a = document.createElement('a');
			a.href = url;
			a.download = 'optimized_resume.docx';
			document.body.appendChild(a);
			a.click();
			a.remove();
			URL.revokeObjectURL(url);
			setStatus('Downloaded optimized DOCX.');
		}else{
			const data = await resp.json();
			resultEl.textContent = data.optimized_resume || '';
			resultEl.hidden = false;
			setStatus('Optimization complete.');
		}
	}catch(err){
		console.error(err);
		setStatus(err.message || 'Request failed');
	}finally{
		setLoading(false);
	}
});