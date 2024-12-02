import os
import polars as pl
import scipy.stats as stats
import numpy as np


def print_interpretation(hyp, result, alpha=0.05):
    interpretation = hyp["H0"] if result.pvalue > alpha else hyp["H1"]
    print(interpretation)
    return interpretation


# Shapiro-Wilk test for normality
def shapiro_wilk(*args):
    # Shapiro-Wilk Test
    result = stats.shapiro(*args, nan_policy="raise")
    print(f"Shapiro-Wilk Test: W={result.statistic}, p={result.pvalue}")

    # Interpretation
    hyp = {
        "H0": "The data is normally distributed.",
        "H1": "The data is not normally distributed.",
    }
    print_interpretation(hyp, result)
    return result


# Test whether the skew is different from the normal distribution.
def skewtest(*args):
    result = stats.skewtest(*args, nan_policy="raise")
    print(f"Skew Test: z={result.statistic}, p={result.pvalue}")

    # Interpretation
    hyp = {
        "H0": "The skew is not significantly different from the normal distribution.",
        "H1": "The skew is significantly different from the normal distribution.",
    }
    print_interpretation(hyp, result)

    return result


# Mann-Whitney U test
def mann_whitney(*args):
    result = stats.mannwhitneyu(*args, nan_policy="raise")
    print(f"Mann-Whitney U Test: H={result.statistic}, p={result.pvalue}")

    # Interpretation
    hyp = {
        "H0": "There is no significant difference between the samples.",
        "H1": "There is a significant difference between the samples.",
    }
    print_interpretation(hyp, result)
    return result


def bootstrap(series: np.typing.ArrayLike, n_iter: int, conf_level: float = 0.95):
    def mean(data, axis):
        return np.mean(data, axis=axis)

    # Perform bootstrap resampling
    bootstrap_result = stats.bootstrap(
        (series,),
        mean,
        confidence_level=conf_level,
        n_resamples=n_iter,
        method="BCa",
        random_state=42,  # For reproducibility
    )

    # Extract the confidence interval
    bootstrap_conf_interval = bootstrap_result.confidence_interval
    print(f"Bootstrap {conf_level*100}% Confidence Interval: {bootstrap_conf_interval}")

    return bootstrap_result


def ensure_dir_exists(directory: str):
    """
    Ensures that the given directory exists. Creates it if it doesn't exist.
    """
    try:
        os.makedirs(directory, exist_ok=True)
    except Exception as e:
        raise RuntimeError(f"Failed to create or access directory '{directory}': {e}")


def to_latex(
    df: pl.DataFrame,
    caption: str,
    label: str,
    confidence_level: float = 0.95,
    na_rep="NULL",
    float_format="{:,.2f}".format,
    latex_dir="outputs/latex/",
):
    ensure_dir_exists(latex_dir)

    ci_string = "\\multicolumn{2}{c}{" + f"{round(confidence_level*100)}\\% CI" + "}"

    if "ci" in df.columns:
        # Unnest the confidence interval column to ci_low and ci_high
        df = df.with_columns(
            pl.col("ci").list.to_struct(fields=["ci_low", "ci_high"]),
        ).unnest("ci")

    latex = (
        df.to_pandas()
        .to_latex(
            index=False,
            caption=caption,
            label=label,
            position="htbp",
            na_rep=na_rep,
            float_format=float_format,
        )
        .replace("ci_low & ci_high", ci_string)
    )

    # Save to file
    filename = label.split(":")[-1]
    out_path = latex_dir + filename + ".tex"
    with open(out_path, "w") as f:
        f.write(latex)

    print(f"Saved to {out_path}")


def draw_ridge_plot(subtitles: pl.DataFrame):
    # Ridge plot (overlapping histograms)

    import seaborn as sns
    import matplotlib.pyplot as plt
    import polars as pl

    sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0)}, font_scale=1.25)

    # Sort entries by mean year within category
    subtitles_by_mean_year = subtitles.with_columns(
        mean_year=pl.col("normalizedYear").mean().over(pl.col("category"))
    ).sort("mean_year")

    pal = sns.cubehelix_palette(10, rot=-0.25, light=0.7)
    g = sns.FacetGrid(
        subtitles_by_mean_year.to_pandas(),
        row="category",
        hue="category",
        aspect=15,
        height=0.5,
        palette=pal,
    )

    # Draw the densities in a few steps
    # g.map(
    #     sns.kdeplot,
    #     "normalizedYear",
    #     bw_adjust=0.5,
    #     clip_on=False,
    #     fill=True,
    #     alpha=1,
    #     linewidth=1.5,
    # )
    # g.map(sns.kdeplot, "normalizedYear", clip_on=False, color="w", lw=2, bw_adjust=0.5)

    # Instead of using kdeplot, use histplot
    g.map(
        sns.histplot,
        "normalizedYear",
        binwidth=5,
        clip_on=False,
        fill=True,
        alpha=1,
        linewidth=1.5,
    )

    # passing color=None to refline() uses the hue mapping
    g.refline(y=0, linewidth=2, linestyle="-", color=None, clip_on=False)

    # Define and use a simple function to label the plot in axes coordinates
    def label(x, color, label):
        ax = plt.gca()
        ax.text(
            0,
            0.2,
            label,
            fontweight="bold",
            color=color,
            ha="left",
            va="center",
            transform=ax.transAxes,
        )

    g.map(label, "normalizedYear")

    # Set the subplots to overlap
    g.figure.subplots_adjust(hspace=-0.25)

    # Remove axes details that don't play well with overlap
    g.set_titles("")
    g.set(yticks=[], ylabel="")
    g.despine(bottom=True, left=True)

    # Set figure size
    fig = plt.gcf()
    fig.set_size_inches(14, 8)

    return g
