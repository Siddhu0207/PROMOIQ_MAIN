"""Pure serialization for the Streamlit UI and CSV export."""
from __future__ import annotations

def flatten_promo(p):
    segs=p.get('segments') or []
    if not segs:
        raise ValueError('Promo has no source segments')
    hook=p.get('hook') or {}
    cliff=p.get('cliffhanger') or {}
    return {
        'episode':'+'.join(str(s['episode']) for s in segs),
        'start':segs[0]['start'],
        'end':segs[-1]['end'],
        'segment_manifest':'; '.join(f"E{s['episode']} {s['start']}–{s['end']}" for s in segs),
        'duration_seconds':p['duration_seconds'],
        'score':(p.get('scores') or {}).get('overall',0),
        'hook':hook.get('text','') if isinstance(hook,dict) else str(hook),
        'cliffhanger':cliff.get('text','') if isinstance(cliff,dict) else str(cliff),
        'why_it_works':p.get('why_it_works',''),
        'approval':'human_video_review_pending',
    }
