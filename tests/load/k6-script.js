// k6 Load Test Script for Inku API
// Run with: k6 run tests/load/k6-script.js

import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');
const mangasLatency = new Trend('mangas_latency');
const chaptersLatency = new Trend('chapters_latency');

// Configuration
const BASE_URL = __ENV.BASE_URL || 'http://localhost:8001';

export const options = {
    // Test stages
    stages: [
        { duration: '30s', target: 10 },   // Ramp up to 10 users
        { duration: '1m', target: 10 },    // Stay at 10 users
        { duration: '30s', target: 50 },   // Ramp up to 50 users
        { duration: '1m', target: 50 },    // Stay at 50 users
        { duration: '30s', target: 0 },    // Ramp down
    ],

    // Thresholds for pass/fail
    thresholds: {
        http_req_duration: ['p(95)<500'],   // 95% of requests < 500ms
        http_req_failed: ['rate<0.01'],     // Error rate < 1%
        errors: ['rate<0.01'],              // Custom error rate < 1%
    },
};

// Main test function
export default function () {
    group('Health Check', () => {
        const healthRes = http.get(`${BASE_URL}/api/health`);
        check(healthRes, {
            'health status is 200': (r) => r.status === 200,
            'health response has status': (r) => r.json('status') === 'ok',
        }) || errorRate.add(1);
    });

    group('Manga Catalog', () => {
        const start = Date.now();
        const mangasRes = http.get(`${BASE_URL}/api/mangas`);
        mangasLatency.add(Date.now() - start);

        const passed = check(mangasRes, {
            'mangas status is 200': (r) => r.status === 200,
            'mangas returns array': (r) => Array.isArray(r.json()),
            'mangas latency < 500ms': (r) => r.timings.duration < 500,
        });

        if (!passed) errorRate.add(1);

        // If we got mangas, test getting chapters for one
        const mangas = mangasRes.json();
        if (mangas && mangas.length > 0) {
            const mangaId = mangas[0].id || mangas[0].manga_id;

            const chaptersStart = Date.now();
            const chaptersRes = http.get(`${BASE_URL}/api/mangas/${mangaId}/chapters`);
            chaptersLatency.add(Date.now() - chaptersStart);

            check(chaptersRes, {
                'chapters status is 200 or 404': (r) => r.status === 200 || r.status === 404,
            }) || errorRate.add(1);
        }
    });

    // Simulate user think time
    sleep(1);
}

// Setup function - runs once before test
export function setup() {
    console.log(`Testing against: ${BASE_URL}`);

    // Verify API is reachable
    const res = http.get(`${BASE_URL}/api/health`);
    if (res.status !== 200) {
        throw new Error(`API not reachable: ${res.status}`);
    }

    return { baseUrl: BASE_URL };
}

// Teardown function - runs once after test
export function teardown(data) {
    console.log(`Test completed against: ${data.baseUrl}`);
}

// Handle test summary
export function handleSummary(data) {
    return {
        'stdout': textSummary(data, { indent: ' ', enableColors: true }),
        'tests/load/results/summary.json': JSON.stringify(data, null, 2),
    };
}

// Text summary helper
function textSummary(data, options) {
    const metrics = data.metrics;

    const lines = [
        '='.repeat(60),
        'Inku API Load Test Results',
        '='.repeat(60),
        '',
        `Total Requests: ${metrics.http_reqs ? metrics.http_reqs.values.count : 0}`,
        `Failed Requests: ${metrics.http_req_failed ? metrics.http_req_failed.values.passes : 0}`,
        '',
        'Response Times:',
        `  Average: ${metrics.http_req_duration ? metrics.http_req_duration.values.avg.toFixed(2) : 0}ms`,
        `  p95: ${metrics.http_req_duration ? metrics.http_req_duration.values['p(95)'].toFixed(2) : 0}ms`,
        `  Max: ${metrics.http_req_duration ? metrics.http_req_duration.values.max.toFixed(2) : 0}ms`,
        '',
        'Thresholds:',
    ];

    for (const [name, threshold] of Object.entries(data.thresholds || {})) {
        const status = threshold.ok ? '✓ PASS' : '✗ FAIL';
        lines.push(`  ${name}: ${status}`);
    }

    lines.push('');
    lines.push('='.repeat(60));

    return lines.join('\n');
}
