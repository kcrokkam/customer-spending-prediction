# Customer Spending Prediction — Project Log

## Project objective
Predict each existing customer's **net spending over the next 30 days**, using only information available before the prediction date.

**Portfolio objective:** Demonstrate reproducible, leakage-safe regression modeling, credible baselines, meaningful visualizations, chronological holdout evaluation, and defensible business conclusions.

## Environment and scope
- Repository: `customer-spending-prediction`
- Environment: GitHub Codespaces, Python
- Dataset: UCI Online Retail II
- Source: `data/raw/online_retail_II.xlsx`, worksheet `Year 2010-2011`
- Existing scripts: `inspect_data.py`, `eda.py`
- Figures: `reports/figures/`
- Raw source dataset must not be committed to Git.
- This log records project progress; the separate learning curriculum is out of scope.

## Checkpoint 1 — Initial inspection (completed)
- Source worksheet: **541,910 rows**, **8 columns**.
- Distinct non-null Customer IDs: **4,372**.
- Rows with missing Customer ID: **135,080**.
- Rows with negative Quantity: **10,624**.
- Rows with nonpositive Price: **2,517**.
- Produced a data-quality bar chart.

**Interpretation:** Customer IDs are needed to build customer histories. Negative quantities may represent returns or cancellations and should not automatically be removed when predicting *net* spending. Counts above are separate diagnostics and may overlap.

## Checkpoint 2 — Cancellation investigation (completed)
- Negative-quantity rows with cancellation-prefixed invoice IDs: **9,288**.
- Other negative-quantity rows: **1,336**; all **1,336** have missing Customer IDs.
- Investigated extreme transactions, including large purchases offset by cancellations.

**Interpretation:** Removing all negative quantities would distort the net-spending outcome. Cancellation invoice prefixes help explain transaction types, but are not by themselves a complete accounting policy.

## Checkpoint 3 — Provisional cleaning (completed)
Current rules:
1. Remove rows without Customer ID.
2. Require `Price > 0`.
3. Retain both positive and negative nonzero quantities.
4. Calculate `LineAmount = Quantity * Price`.

**Observed result:** **406,790** cleaned line-item rows, including **8,905** cancellation-prefixed rows.

**Decision status: provisional.** Before modeling, verify timestamp parsing, duplicate policy, invoice/return handling, and the effect of cancellations whose original purchases may lie outside the observation window. Avoid using future returns as features for earlier prediction dates.

## Checkpoint 4 — Customer spending distribution (in progress)
- Started aggregation of customer-level net spending.
- Prepared a histogram that excludes the top 1% of positive spenders **for visualization only**.
- The simplified `eda.py` has **not yet been run and interpreted at this checkpoint**.

**Next action:** Run `python eda.py`, inspect the printed customer-spending summary and generated histogram, and record observed values and findings here. Do not assume a skew, customer count, or specific quantile until confirmed by output.

**EDA interpretation questions:**
- What are the count, mean, median, standard deviation, minimum, maximum, and 90th/99th percentiles of customer-level net spending?
- How many customers have zero or negative net spending?
- How concentrated is spending among the highest-spending customers?
- Does excluding the top 1% improve histogram readability without hiding important business behavior?

## Modeling plan (not started)
1. Define prediction dates and eligible existing customers.
2. Build a **future 30-day net-spending target** from transactions after each prediction date.
3. Build customer features using transactions available **strictly before** each prediction date; determine history window and treatment of no-purchase customers.
4. Use chronological train/validation/test partitions, with appropriate attention to overlapping 30-day label windows and the availability of labels at model training time.
5. Compare simple baselines (such as zero spend and historical-spend-based predictions) with regression models.
6. Evaluate on untouched chronological test data with MAE, RMSE, R², and segment-level errors; compare against baselines.
7. Document limitations, business implications, reproducibility, and final results without overstating performance.

## Pending decisions and cautions
- Decide whether net spending can be negative and whether negative targets should be retained (default: preserve genuine net outcomes).
- Specify transaction timestamp boundaries and the treatment of purchases/returns at prediction cutoffs.
- Determine customer eligibility at each prediction date, including customers who do not buy during the future 30 days.
- Avoid fitting transformations or selecting model hyperparameters using holdout test information.
- Keep source data excluded from commits; verify `.gitignore` before publishing.

## Next checkpoint
**Run and interpret customer-level net-spending EDA.** Append the actual printed statistics, figure name, interpretation, and any methodological decisions to this log. Then commit the documentation and confirmed EDA checkpoint.
