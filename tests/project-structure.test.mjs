import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import test from 'node:test';
import { resolve } from 'node:path';

const requiredPaths = [
  'frontend/src/components',
  'frontend/src/pages',
  'frontend/src/services',
  'frontend/src/styles',
  'backend/app/routes',
  'backend/app/controllers',
  'backend/app/services',
  'backend/app/models',
  'backend/app/middleware',
  'backend/app/utils',
  'backend/tests/test_health.py',
  'backend/pyproject.toml',
  'frontend/src/app',
  'frontend/vitest.config.ts',
  'frontend/playwright.config.ts',
  'database',
  'docker',
  'docs',
  '.env.example',
  '.env.development',
  '.env.production',
];

test('defines the initial project structure', () => {
  for (const path of requiredPaths) {
    assert.equal(existsSync(resolve(path)), true, `Missing required path: ${path}`);
  }
});

test('declares scripts for the approved technology stack', () => {
  const manifest = JSON.parse(readFileSync(resolve('package.json'), 'utf8'));

  assert.deepEqual(manifest.workspaces, ['frontend']);
  assert.equal(typeof manifest.scripts.dev, 'string');
  assert.equal(typeof manifest.scripts.build, 'string');
  assert.equal(typeof manifest.scripts.test, 'string');
  assert.equal(typeof manifest.scripts.lint, 'string');
  assert.equal(typeof manifest.scripts.typecheck, 'string');
  assert.match(manifest.scripts['dev:backend'], /uvicorn/);
  assert.match(manifest.scripts.test, /pytest/);
  const frontendManifest = JSON.parse(readFileSync(resolve('frontend/package.json'), 'utf8'));
  assert.match(frontendManifest.scripts.test, /vitest/);
  assert.match(frontendManifest.scripts['test:e2e'], /playwright/);
});

test('provides templates for database, session, and storage configuration', () => {
  for (const fileName of ['.env.example', '.env.development', '.env.production']) {
    const environmentFile = readFileSync(resolve(fileName), 'utf8');

    assert.match(environmentFile, /^DATABASE_URL=/m);
    assert.match(environmentFile, /^SESSION_SECRET=/m);
    assert.match(environmentFile, /^STORAGE_PATH=/m);
  }
});

test('provides reproducible local container infrastructure', () => {
  const compose = readFileSync(resolve('docker-compose.yml'), 'utf8');
  for (const path of [
    'docker/backend.Dockerfile',
    'docker/frontend.Dockerfile',
    'docker/backend.Dockerfile.dockerignore',
    'docker/frontend.Dockerfile.dockerignore',
    'docker/nginx.conf',
    'scripts/setup-dev.ps1',
    'frontend/next.config.mjs',
  ]) {
    assert.equal(existsSync(resolve(path)), true, `Missing infrastructure file: ${path}`);
  }

  assert.match(compose, /database:/);
  assert.match(compose, /backend:/);
  assert.match(compose, /frontend:/);
  assert.match(compose, /postgres_data:/);
  assert.match(compose, /voucher_storage:/);
  assert.match(compose, /condition: service_healthy/);
  assert.match(compose, /\/api\/health/);
});
