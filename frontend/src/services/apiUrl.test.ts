import { describe, expect, it } from 'vitest';

import { getApiUrl } from './apiUrl';

describe('getApiUrl', () => {
  it('uses the local FastAPI endpoint by default', () => {
    expect(getApiUrl()).toBe('http://localhost:8000/api');
  });
});
