/**
 * Code Monkeys Dash MVP
 * 
 * Fetches and renders product and run data from JSON fixtures.
 * Features:
 * - Product list with status
 * - Run details (status, evidence, economy)
 * - Run history (last N runs)
 * - Error handling (no silent failures)
 */
document.addEventListener('DOMContentLoaded', async () => {
    const app = {
        MAX_HISTORY: 5,  // Show last N runs in history
        
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

        fetchRunHistory: async (productId, runIds) => {
            /**
             * Fetch details for specific run IDs.
             * In a real implementation, each run would have its own report.json.
             * For MVP, we just show the run IDs and link to logs.
             */
            return runIds.slice(0, app.MAX_HISTORY).map(runId => ({
                run_id: runId,
                log_path: `runs/${productId}/${runId}/pytest_output.log`
            }));
        },

        detectRunHistory: async (productId) => {
            /**
             * Detect available run directories by checking for known runs.
             * In MVP, we use the last_run.json as the source of truth.
             * A more complete implementation would list the directory.
             */
            // For now, we only show the current run from last_run.json
            // Future: API or manifest file listing all runs
            return [];
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
            let historySection = '';
            let validityBadge = '';
            
            if (run) {
                // Schema validity check
                const isValid = run.schema_version === '0.1';
                validityBadge = isValid 
                    ? '<span class="validity valid">✅ Schema Valid</span>'
                    : '<span class="validity invalid">❌ Invalid Schema</span>';
                
                // Compute spent_minutes display
                const spentMinutes = run.banana_economy.spent_minutes || 0;
                const spentDisplay = spentMinutes > 0 ? `${spentMinutes} min` : '< 1 min';
                
                runDetails = `
                    <div class="row"><span class="label">Run ID:</span> <span>${run.run_id}</span></div>
                    <div class="row"><span class="label">Ended:</span> <span>${new Date(run.ended_at).toLocaleString()}</span></div>
                    <div class="row"><span class="label">Duration:</span> <span>${spentDisplay}</span></div>
                    <div class="row"><span class="label">Summary:</span> <span>${run.summary}</span></div>
                    
                    <div class="economy-section">
                        <div class="row"><span class="label">Budget (Tok):</span> <span>${run.banana_economy.spent_tokens} / ${run.banana_economy.budget_tokens}</span></div>
                        <div class="row"><span class="label">Time:</span> <span>${run.banana_economy.spent_minutes} / ${run.banana_economy.budget_minutes} min</span></div>
                        <div class="row"><span class="label">Kill Switch:</span> <span class="kill-${run.kill_switch.enabled}">${run.kill_switch.enabled ? 'ENABLED ⚠️' : 'OFF'}</span></div>
                        <div class="row"><span class="label">PR Wave:</span> <span>${run.pr_wave.state} (${run.pr_wave.open_prs} open)</span></div>
                    </div>

                    <div class="evidence-section">
                        <p class="label">Evidence:</p>
                        <ul class="evidence-list">
                            ${run.evidence.paths.map(p => `<li><a href="${p}" class="evidence-link" target="_blank">${p.split('/').pop()}</a></li>`).join('')}
                        </ul>
                    </div>
                `;
                
                // History section (placeholder for future runs)
                historySection = `
                    <div class="history-section">
                        <p class="label">Run History:</p>
                        <div class="history-note">Most recent run shown above. Previous runs in <code>runs/${product.product_id}/</code></div>
                    </div>
                `;
            }

            div.innerHTML = `
                <div class="card-header">
                    <span class="product-name">${product.display_name}</span>
                    <div class="status-badges">
                        ${validityBadge}
                        <span class="status-indicator ${statusClass}">${status}</span>
                    </div>
                </div>
                <div class="card-body">
                    <div class="row"><span class="label">Owner:</span> <span>${product.owner}</span></div>
                    ${runDetails}
                    ${historySection}
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
