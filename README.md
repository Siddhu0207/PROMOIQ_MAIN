# PromoIQ — Microdrama Promo Discovery

**Kuku AI Generalist | Problem 1: Find the Promos**

PromoIQ reads timecoded screenplay text and selects **20–60-second promo windows** with an immediate hook (first 3 seconds), an unresolved ending and a standalone narrative. Each output has an episode ID, timestamp boundaries, hook, cliffhanger, rationale and relative ranking. No edits, music or overlays are produced.

The deterministic prototype was validated on a **supplied pack of 50 episodes**. The full-run outputs are a **separate submission artifact**, rather than training or input material published to GitHub. Source screenplays are deliberately **not included in this public-ready repository**, pending confirmation of redistribution rights.

## Quick start: no account, API, installation or source screenplay required

Python 3.10+ (only standard library for the CLI):

```bash
python3 -m unittest discover -s tests -v
python3 run_pipeline.py --episode 099 --source-dir examples --input-dir demo_processed --output-dir demo_outputs --force
```

Open `demo_outputs/ranked_promos.csv` to inspect the generated promo, or check `demo_outputs/promotional_candidates/episode_099_promos.json` for the detailed segment. **Episode 099 is wholly fictional**, created solely to demonstrate an executable public repo.

## Optional interactive Streamlit app

```bash
python3 -m pip install -r requirements-streamlit.txt
streamlit run app.py
```

Use *Try fictional demo* or upload timestamped `.txt` screenplay files. The UI displays ranked promos and allows CSV export. To deploy it on [Streamlit Community Cloud](https://share.streamlit.io/), connect the public GitHub repo, select `app.py` as its entry point and Streamlit Cloud automatically reads the root `requirements.txt`, which includes the UI dependency. The CLI itself still works without any pip installation.

**Note:** The optional `app.py` interface is prepared and syntax-checked, but Streamlit wasn't installed in the preparation environment. Deploy and verify it under your own account before submitting an app URL. The GitHub repository itself is an accepted prototype format.

## Reproduce the full Kuku input-pack run (locally, with permission)

Place the 50 supplied `episode-*.txt` files into `data/raw/`; do not publish the original scripts without authorization.

```bash
python3 run_pipeline.py --episode 003 --force
python3 run_pipeline.py --all --auto-sample-gate --experimental-stitches --force
python3 compare_baseline.py
python3 evaluate_quality.py prepare --set human_evaluation
python3 evaluate_quality.py score --set human_evaluation
python3 evaluate_quality.py prepare --set human_evaluation_v2
python3 evaluate_quality.py score --set human_evaluation_v2
python3 -m unittest discover -s tests_full_pack -v
```

Main outputs:

- `outputs/ranked_promos.csv` — ordered continuous promo windows, hooks and cliffhangers.
- `outputs/POST_FIRST_20.md` — unique-episode posting order and reasons.
- `outputs/promotional_candidates/` — per-episode JSON and stitched experimental manifests.
- `outputs/quality_reports/` — structural QA, rejection reasons and review notes.
- `outputs/execution_benchmark.json` — actual measured text-only runtime.
- `outputs/baseline_comparison.json` — fixed-first-40s baseline, **structural evidence, not empirical performance**.

Two provenance-specific tests of Episode 003 prior LLM annotations skip automatically if the private `data/legacy/` file is not present in a fresh public clone; the private original package has it and passes all 42. The `prepare` commands build blank packet sheets; running `score` on blank sheets creates honest `awaiting_two_independent_human_reviews` status (no invented acceptance rates). The test suite requires these generated evaluation-status files. Run `score` again **after** two independent people actually rate the clips to obtain empirical quality figures.

## Evaluation snapshot (from the supplied 50-episode local run)

| Result | Value |
|---|---:|
| Episodes parsed | 50 |
| Timestamped events | 3,727 |
| Hook candidates | 694 |
| Cliffhanger anchors | 139 |
| Ranked continuous promo candidates | 75 across 34 episodes |
| Structurally validated stitched experiments | 7 (not editorially approved) |
| Regression tests, with the full pack | 42 passed |
| Rule-based model calls / paid API cost | 0 / $0 |

The project intentionally leaves **16 episodes without a qualifying promo**. No human approval, video validation, watch-through or conversion metrics have been claimed.

## How it works

1. `src/parser.py` preserves scene timestamps and actions/dialogue/camera/sound.
2. `src/scene_analyzer.py` records evidence at the scene level.
3. `src/hook_detector.py` considers physical and verbal actions at potential openings.
4. `src/promo_generator.py` constructs and ranks duration-valid clips; `src/editorial_guard.py` screens risky openings/endings and `src/quality_check.py` validates cuts.
5. `src/stitch_quality.py` ranks **experimental** stitched alternatives without claiming video continuity.
6. `src/evaluation.py` prepares blinded independent-review samples.

The optional local Ollama reviewer (`src/llm_review.py`) is implemented but was **not executed** for the reported full-pack run. Heuristic scores are ranking aids, not performance predictions.

## Known failures (and what was fixed)

- Episode 047 previously labeled a plea as a physical rescue cliffhanger; the stricter gate rejects the unsupported label.
- A candle-only establishing shot falsely triggered a hook; the opening gate now requires corroborating action/dialogue.
- Episode 028 physically yanks a locket at the opening; the simultaneous-event change recovers this true hook.
- Episode 042's already-completed Duke reveal and Episode 024's completed vow are rejected as unresolved cliffhangers.
- Candidate evaluation packets previously contained significant overlaps; v2 suppresses near-duplicates.

Remaining challenges include ambiguous context, visual timing mismatch, incomplete human review and unknown engagement effectiveness.

## Dependencies and rights

For the CLI and testing, the Python standard library is enough. The optional Streamlit app requires the `streamlit` dependency in `requirements.txt` (duplicated in `requirements-streamlit.txt` for clarity). This repository's synthetic demo is original; the supplied production screenplays and the full unedited review packets have separate sharing and rights requirements.

See the two-page solution PDF and unedited full-run outputs in the separate submission artifacts.
