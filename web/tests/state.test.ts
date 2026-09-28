import { describe, expect, it } from 'vitest';
import { decodeState, encodeState } from '../src/lib/state/codec';
import { makeDefaultState } from '../src/lib/state/types';

describe('iOS-compatible backup format', () => {
  it('round-trips the default state', () => {
    const state = makeDefaultState();
    state.startDate = '2026-09-01T00:00:00Z';
    state.bookmarks.push({
      id: 'A1B2C3D4-0000-4000-8000-000000000000',
      documentID: 'quick.reference',
      sectionID: 'quick.reference.overview',
      title: 'Quick Reference',
      note: 'Read before every mock',
      createdAt: '2026-09-02T10:00:00Z',
      updatedAt: '2026-09-02T10:00:00Z',
    });
    const result = decodeState(encodeState(state));
    expect(result.ok && result.state).toEqual(state);
  });

  it('encodes weeklyProgress as Swift does for [Int: WeekProgress]', () => {
    const json = JSON.parse(encodeState(makeDefaultState()));
    expect(Array.isArray(json.weeklyProgress)).toBe(true);
    expect(json.weeklyProgress[0]).toBe(1);
    expect(json.weeklyProgress[1].week).toBe(1);
    expect(json.weeklyProgress).toHaveLength(24);
  });

  it('never writes fractional seconds (Swift .iso8601 rejects them)', () => {
    const state = makeDefaultState();
    state.interviewDate = '2026-12-01T09:30:00Z';
    expect(encodeState(state)).not.toMatch(/\d{2}:\d{2}:\d{2}\.\d+Z/);
  });

  it('accepts Swift reference-date numbers and object-keyed weeks', () => {
    const state = JSON.parse(encodeState(makeDefaultState()));
    state.startDate = 0; // 2001-01-01T00:00:00Z
    state.weeklyProgress = { 3: { ...state.weeklyProgress[5], week: 3, status: 'In Progress' } };
    const result = decodeState(JSON.stringify(state));
    expect(result.ok).toBe(true);
    if (result.ok) {
      expect(result.state.startDate).toBe('2001-01-01T00:00:00Z');
      expect(result.state.weeklyProgress[3]!.status).toBe('In Progress');
      expect(Object.keys(result.state.weeklyProgress)).toHaveLength(12);
    }
  });

  it('applies the iOS validation rules', () => {
    const state = JSON.parse(encodeState(makeDefaultState()));
    state.weeklyProgress[1].independentlySolved = 5;
    const result = decodeState(JSON.stringify(state));
    expect(result.ok).toBe(false);
    expect(!result.ok && result.error).toMatch(/cannot exceed attempted/);
    expect(decodeState('{"version": 2}')).toMatchObject({ ok: false });
    expect(decodeState('not json')).toMatchObject({ ok: false, error: 'The file is not valid JSON.' });
  });
});
