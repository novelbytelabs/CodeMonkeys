/**
 * Code Monkeys Dash MVP
 * 
 * Fetches and renders product and run data from JSON fixtures.
 * Features:
 * - Product list with status
 * - Run details (status, evidence, economy)
 * - Nexus queue (pending requests + decisions)
 * - Error handling (no silent failures)
 */
document.addEventListener('DOMContentLoaded', async () => {
    const app = {
        MAX_HISTORY: 5,
        
        init: async () => {
            try {
                const products = await app.fetchProducts();
                await app.renderProducts(products);
                await app.renderNexusQueue();
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

        fetchNexusInbox: async () => {
            // Try to fetch known inbox files (in production, this would be a manifest)
            const requests = [];
            const knownRequests = ['req_20251221_001'];
            for (const reqId of knownRequests) {
                try {
                    const response = await fetch(`../nexus/inbox/${reqId}.json`);
                    if (response.ok) {
                        requests.push(await response.json());
                    }
                } catch (e) {
                    // Skip on error
                }
            }
            return requests;
        },

        fetchNexusOutbox: async () => {
            const decisions = [];
            const knownDecisions = ['dec_20251221_001'];
            for (const decId of knownDecisions) {
                try {
                    const response = await fetch(`../nexus/outbox/${decId}.json`);
                    if (response.ok) {
                        decisions.push(await response.json());
                    }
                } catch (e) {
                    // Skip on error
                }
            }
            return decisions;
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

        renderNexusQueue: async () => {
            const container = document.getElementById('nexus-pending');
            container.innerHTML = '';

            const requests = await app.fetchNexusInbox();
            const decisions = await app.fetchNexusOutbox();

            if (requests.length === 0 && decisions.length === 0) {
                container.innerHTML = '<div class="empty-state">No pending requests or decisions</div>';
                return;
            }

            // Render pending requests
            for (const req of requests) {
                const card = app.createNexusRequestCard(req);
                container.appendChild(card);
            }

            // Render recent decisions
            for (const dec of decisions) {
                const card = app.createNexusDecisionCard(dec);
                container.appendChild(card);
            }
        },

        createNexusRequestCard: (req) => {
            const div = document.createElement('div');
            div.className = 'card nexus-card';
            const statusClass = `status-${req.status}`;
            const priorityClass = `priority-${req.priority || 'normal'}`;

            div.innerHTML = `
                <div class="card-header">
                    <span class="product-name">📥 ${req.type.replace('_', ' ')}</span>
                    <span class="status-indicator ${statusClass}">${req.status}</span>
                </div>
                <div class="card-body">
                    <div class="row"><span class="label">Request:</span> <span>${req.request_id}</span></div>
                    <div class="row"><span class="label">Source:</span> <span>${req.source}</span></div>
                    <div class="row"><span class="label">Priority:</span> <span class="${priorityClass}">${req.priority || 'normal'}</span></div>
                    <div class="row"><span class="label">Created:</span> <span>${new Date(req.created_at).toLocaleString()}</span></div>
                </div>
            `;
            return div;
        },

        createNexusDecisionCard: (dec) => {
            const div = document.createElement('div');
            div.className = 'card nexus-card decision';
            const statusClass = `status-${dec.status}`;

            div.innerHTML = `
                <div class="card-header">
                    <span class="product-name">📤 ${dec.type.replace('_', ' ')}</span>
                    <span class="status-indicator ${statusClass}">${dec.status}</span>
                </div>
                <div class="card-body">
                    <div class="row"><span class="label">Decision:</span> <span>${dec.decision_id}</span></div>
                    <div class="row"><span class="label">Target:</span> <span>${dec.target}</span></div>
                    <div class="row"><span class="label">Rationale:</span> <span>${dec.rationale || 'N/A'}</span></div>
                    ${dec.governance_check ? `
                        <div class="row"><span class="label">Governance:</span> 
                            <span class="governance-${dec.governance_check.compliant ? 'ok' : 'fail'}">
                                ${dec.governance_check.compliant ? '✅ Compliant' : '❌ Violation'}
                            </span>
                        </div>
                    ` : ''}
                </div>
            `;
            return div;
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
                const isValid = run.schema_version === '0.1';
                validityBadge = isValid 
                    ? '<span class="validity valid">✅ Schema Valid</span>'
                    : '<span class="validity invalid">❌ Invalid Schema</span>';
                
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
