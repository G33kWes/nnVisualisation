# Master: nnVisualisation reproduction process

This master file lists the ordered steps an agent
should follow to reproduce the `nnVisualisation` project from scratch.

## Steps (in recommended order)
1. `.gitignore` — see `steps/01_.gitignore.md` for details
2. `assets` — see `steps/02_assets.md` for details
3. `deploy.sh` — see `steps/03_deploy.sh.md` for details
4. `exports` — see `steps/04_exports.md` for details
	- Substep: manifest & snapshots — see `steps/04_exports__01_manifest_and_snapshots.md`
5. `index.html` — see `steps/05_index.html.md` for details
6. `README.md` — see `steps/06_README.md.md` for details
7. `tools` — see `steps/07_tools.md` for details
	- Substep: mnist assets — see `steps/07_tools__01_mnist_assets.md`
8. `training` — see `steps/08_training.md` for details
	- Substep: training/mlp_train.py — see `steps/08_training__01_mlp_train.md`

## Agent workflow guidance
See `README_agent.md` for detailed instructions the agent should follow (one step at a time,
run tests, request human approval, then continue).