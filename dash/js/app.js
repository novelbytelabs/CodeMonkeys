document.addEventListener('DOMContentLoaded', async () => {
    const app = {
        init: async () => {
            try {
                const products = await app.fetchProducts();
                await app.renderProducts(products);
                document.getElementById('loading').classList.add('hidden');
                document.getElementById('dashboard').classList.remove('hidden');
            } catch (err) {
                app.showError(err.message);
            }
        },

        fetchProducts: async () => {
            const response = await fetch('products.json');
            if (!response.ok) throw new Error('Failed to load products.json');
            const data = await response.json();
            return data.products;
        },

        fetchLastRun: async (productId) => {
            try {
                const response = await fetch(`runs/${productId}/last_run.json`);
                if (!response.ok) return null;
                return await response.json();
            } catch (e) {
                return null;
            }
        },

        renderProducts: async (products) => {
            const list = document.getElementById('products-list');
            list.innerHTML = '';

            for (const product of products) {
                const runData = await app.fetchLastRun(product.product_id);
                const card = app.createProductCard(product, runData);
                list.appendChild(card);
            }
        },

        createProductCard: (product, run) => {
            const div = document.createElement('div');
            div.className = 'card';
            
            const status = run ? run.status : product.status;
            const statusClass = `status-${status}`;

            let runDetails = '<div class="row"><span class="label">Status:</span> <span>No Run Data</span></div>';
            
            if (run) {
                runDetails = `
                    <div class="row"><span class="label">Run ID:</span> <span>${run.run_id}</span></div>
                    <div class="row"><span class="label">Ended:</span> <span>${new Date(run.ended_at).toLocaleString()}</span></div>
                    <div class="row"><span class="label">Summary:</span> <span>${run.summary}</span></div>
                    
                    <div class="economy-section">
                        <div class="row"><span class="label">Budget (Tok):</span> <span>${run.banana_economy.spent_tokens} / ${run.banana_economy.budget_tokens}</span></div>
                        <div class="row"><span class="label">Kill Switch:</span> <span>${run.kill_switch.enabled ? 'ENABLED' : 'OFF'}</span></div>
                    </div>

                    <div class="evidence-section">
                        <p class="label">Evidence:</p>
                        <ul class="evidence-list">
                            ${run.evidence.paths.map(p => `<li><a href="${p}" class="evidence-link" target="_blank">${p}</a></li>`).join('')}
                        </ul>
                    </div>
                `;
            }

            div.innerHTML = `
                <div class="card-header">
                    <span class="product-name">${product.display_name}</span>
                    <span class="status-indicator ${statusClass}">${status}</span>
                </div>
                <div class="card-body">
                    <div class="row"><span class="label">Owner:</span> <span>${product.owner}</span></div>
                    ${runDetails}
                </div>
            `;
            return div;
        },

        showError: (msg) => {
            const el = document.getElementById('error');
            el.textContent = `Error: ${msg}`;
            el.classList.remove('hidden');
            document.getElementById('loading').classList.add('hidden');
        }
    };

    app.init();
});
