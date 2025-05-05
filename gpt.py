import math
import numpy as np
from scipy.stats import chi2, t
from scipy.odr import ODR, Model, RealData
from typing import Sequence, Optional, Tuple, Union


def mean(values: Sequence[float]) -> float:
    """
    Compute the arithmetic mean of a sequence of numbers.
    """
    return float(np.mean(values))


def weighted_mean(values: Sequence[float], uncertainties: Sequence[float]) -> float:
    """
    Compute the weighted mean of values with associated uncertainties.
    weights = 1 / uncertainties**2
    """
    values_arr = np.asarray(values, dtype=float)
    sigma = np.asarray(uncertainties, dtype=float)
    w = 1.0 / sigma**2
    return float(np.sum(values_arr * w) / np.sum(w))


def weighted_mean_uncertainty(uncertainties: Sequence[float]) -> float:
    """
    Uncertainty of the weighted mean.
    """
    sigma = np.asarray(uncertainties, dtype=float)
    return float(np.sqrt(1.0 / np.sum(1.0 / sigma**2)))


def sample_std(values: Sequence[float]) -> float:
    """
    Compute the sample standard deviation (ddof=1).
    """
    return float(np.std(values, ddof=1))


def covariance(x: Sequence[float], y: Sequence[float]) -> float:
    """
    Compute the sample covariance between two datasets.
    """
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)
    return float(np.cov(x_arr, y_arr, ddof=1)[0, 1])


def pearson_r(x: Sequence[float], y: Sequence[float]) -> float:
    """
    Compute Pearson's correlation coefficient.
    """
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)
    return float(np.corrcoef(x_arr, y_arr)[0, 1])


def pearson_uncertainty(r: float, n: int) -> float:
    """
    Uncertainty of Pearson's r: sqrt((1 - r**2)/(n - 2))
    """
    return math.sqrt((1.0 - r**2) / (n - 2))


def posterior_error(x: Sequence[float], y: Sequence[float], intercept: float, slope: float) -> float:
    """
    Posterior (residual) standard error for linear fit.
    """
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)
    resid = y_arr - (intercept + slope * x_arr)
    return float(np.sqrt(np.sum(resid**2) / (len(x_arr) - 2)))


def linear_fit_orthogonal(
    x: Sequence[float],
    y: Sequence[float],
    x_unc: Optional[Sequence[float]] = None,
    y_unc: Optional[Sequence[float]] = None,
    initial: Tuple[float, float] = (0.0, 1.0)
) -> Tuple[float, float, float, float, float]:
    """
    Perform an ODR linear fit (y = a + b x) with optional uncertainties.

    Returns:
        a, b, sigma_a, sigma_b, covariance_ab
    """
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)
    sx = np.zeros_like(x_arr) if x_unc is None else np.asarray(x_unc, dtype=float)
    sy = np.ones_like(y_arr) if y_unc is None else np.asarray(y_unc, dtype=float)

    data = RealData(x_arr, y_arr, sx=sx, sy=sy)
    model = Model(lambda B, x_val: B[0] + B[1] * x_val)
    odr = ODR(data, model, beta0=list(initial))
    out = odr.run()

    a, b = out.beta
    sigma_a, sigma_b = out.sd_beta
    cov_ab = out.cov_beta[0, 1]
    return float(a), float(b), float(sigma_a), float(sigma_b), float(cov_ab)


def chi_square_goodness_of_fit(
    x: Sequence[float],
    y: Sequence[float],
    y_unc: Sequence[float],
    intercept: float,
    slope: float,
    ddof: int = 2
) -> Tuple[float, int, float]:
    """
    Compute chi-square, degrees of freedom, and p-value for linear fit.

    Returns:
        chi2_value, dof, p_value
    """
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)
    sy = np.asarray(y_unc, dtype=float)
    y_pred = intercept + slope * x_arr
    chi2_val = float(np.sum(((y_arr - y_pred) / sy) ** 2))
    dof = len(x_arr) - ddof
    p_val = chi2.sf(chi2_val, dof)
    return chi2_val, dof, p_val


# Utility __main__ for script usage
def main():
    import argparse

    parser = argparse.ArgumentParser(description="Linear regression analysis with uncertainties.")
    parser.add_argument("--x", nargs="+", type=float, required=True, help="X data points")
    parser.add_argument("--y", nargs="+", type=float, required=True, help="Y data points")
    parser.add_argument(
        "--sy", nargs="+", type=float,
        help="Y uncertainties (uniform if single value)"
    )
    parser.add_argument(
        "--sx", nargs="+", type=float,
        help="X uncertainties (uniform if single value)"
    )
    parser.add_argument("--output", type=str, default="analysis.txt", help="Output filename")
    args = parser.parse_args()

    # Example execution
    a, b, sa, sb, cov_ab = linear_fit_orthogonal(args.x, args.y, args.sx, args.sy)
    chi2_val, dof, p_val = chi_square_goodness_of_fit(args.x, args.y, args.sy or [1]*len(args.y), a, b)

    with open(args.output, 'w') as f:
        f.write(f"Fit: y = {a:.5f} ± {sa:.5f} + ({b:.5f} ± {sb:.5f}) x\n")
        f.write(f"Cov(a,b) = {cov_ab:.5f}\n")
        f.write(f"Chi2 = {chi2_val:.2f}, dof = {dof}, p = {p_val:.3f}\n")


if __name__ == "__main__":
    main()
