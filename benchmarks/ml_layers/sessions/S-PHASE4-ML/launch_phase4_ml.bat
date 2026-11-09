@echo off
setlocal EnableExtensions
REM ===================================================================
REM  S-PHASE4-ML launcher: fetch the ML-layer branch into D:\wt-phase4-ml
REM  (a separate git worktree, so D:\ and the other session's uncommitted
REM  work are never touched), then run tests / experiments from a menu.
REM ===================================================================
set "REPO=D:\"
set "BRANCH=claude/relaxed-mendel-k3gpne"
set "WT=D:\wt-phase4-ml"
set "PKG=%WT%\PDEFactorML"
set "PY=D:\PDEFactorML\.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"

echo.
echo [1/2] Fetching %BRANCH% ...
git -c safe.directory=D:/ -C %REPO% fetch origin %BRANCH% || goto :fail
if exist "%WT%\.git" (
    echo Updating existing worktree %WT% ...
    git -c safe.directory=* -C "%WT%" checkout --detach origin/%BRANCH% || goto :fail
) else (
    echo Creating worktree %WT% ...
    git -c safe.directory=D:/ -C %REPO% worktree add --detach "%WT%" origin/%BRANCH% || goto :fail
)

REM the worktree's code wins over the venv's editable install of D:\PDEFactorML
set "PYTHONPATH=%PKG%\src;%PKG%"
REM results of the session are needed by E14: copy the corpus where the scripts expect it
if not exist "%PKG%\analysis\exp\out" mkdir "%PKG%\analysis\exp\out"
copy /Y "%PKG%\sessions\S-PHASE4-ML\results\e13_corpus.jsonl" "%PKG%\analysis\exp\out\" >nul

echo [2/2] Python: %PY%
"%PY%" -c "import numpy, scipy, sklearn; print('numpy', numpy.__version__, 'scipy', scipy.__version__, 'sklearn', sklearn.__version__)" || (
    echo Missing packages. Install with:  "%PY%" -m pip install numpy scipy sympy scikit-learn torch gpytorch
    goto :fail
)

:menu
echo.
echo ================= S-PHASE4-ML =================
echo  Files are in: %PKG%
echo  1  Run the ML-layer tests (tests\test_learned.py, ~2-7 min)
echo  2  E14  calibration on held-out families (seconds; uses the shipped corpus)
echo  3  E15  seed upper bound: control / ESPIRA / oracle (~15 min)
echo  4  E16  raw-data scan vs GP path, heat 400 pts 5%% (~10-30 min, needs gpytorch)
echo  5  E13  rebuild the 126-run corpus (long: ~1-3 h, 4 workers)
echo  6  E12  retrain L0 and compare (long: ~1 h CPU, needs torch)
echo  7  Open the file index and the report
echo  8  Run the whole test suite
echo  0  Exit
echo ===============================================
set "CH="
set /p "CH=Choice: "
if "%CH%"=="1" ( pushd "%PKG%" & "%PY%" -m pytest -q tests\test_learned.py & popd & goto :menu )
if "%CH%"=="2" ( pushd "%PKG%" & "%PY%" analysis\exp\e14_calibration.py & popd & goto :menu )
if "%CH%"=="3" ( pushd "%PKG%" & "%PY%" analysis\exp\e15_seed_bounds.py --n 500 & popd & goto :menu )
if "%CH%"=="4" ( pushd "%PKG%" & "%PY%" analysis\exp\e16_raw_scan.py --seeds 3 & popd & goto :menu )
if "%CH%"=="5" ( pushd "%PKG%" & "%PY%" analysis\exp\e13_corpus.py --workers 4 --seeds 2 & popd & goto :menu )
if "%CH%"=="6" ( pushd "%PKG%" & "%PY%" analysis\exp\e12_l0_seeds.py --train 12000 --n 1500 & popd & goto :menu )
if "%CH%"=="7" ( start "" "%PKG%\sessions\S-PHASE4-ML\INDICE.md" & start "" "%PKG%\sessions\S-PHASE4-ML\REPORT.md" & goto :menu )
if "%CH%"=="8" ( pushd "%PKG%" & "%PY%" -m pytest -q & popd & goto :menu )
if "%CH%"=="0" goto :end
echo Unknown choice.
goto :menu

:fail
echo.
echo *** Something failed (see above). ***
pause
exit /b 1

:end
echo New results are written to %PKG%\analysis\exp\out\
endlocal
