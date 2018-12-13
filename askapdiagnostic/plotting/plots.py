#!/usr/bin/env python

import logging
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches
from matplotlib.lines import Line2D

logger = logging.getLogger(__name__)


def flux_ratio_image_view(df, title="Flux ratio plot", save=True):
    # filter_df=df[df["d2d"]<=maxsep].reset_index(drop=True)
    # ratios=filter_df["askap_int_flux"]/(filter_df["sumss_St"]/1.e3).values
    #sloppy check
    mask=[True if i < 5. else False for i in df["askap_sumss_int_flux_ratio"]]
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)
    ratio_plot=ax.scatter(df["askap_ra"].values[mask], df["askap_dec"].values[mask], c=df["askap_sumss_int_flux_ratio"][mask], cmap="Reds", marker="o")
    cb=plt.colorbar(ratio_plot, ax=ax)
    cb.set_label("ASKAP / SUMSS flux ratio")
    plt.xlabel("RA (deg)")
    plt.ylabel("Dec (deg)")
    plt.gca().invert_xaxis()
    
    plt.title(title)
    
    if save:
        logger.info("Plot saved")
        plt.savefig("flux_ratio_location_pandas.png", bbox_inches="tight")
    plt.close()
    
    
def position_offset(df, title="Position offset plot", save=True):
    # filter_df=df[df["d2d"]<=maxsep]
    ra_offset=df["askap_sumss_ra_offset"]*3600.
    dec_offset=df["askap_sumss_dec_offset"]*3600.
    med_ra_offset=ra_offset.median()
    med_dec_offset=dec_offset.median()
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)
    beam=patches.Ellipse((0,0), df.iloc[0]["askap_psf_a"],df.iloc[0]["askap_psf_b"], df.iloc[0]["askap_psf_pa"], 
         edgecolor="k", facecolor="gold", fill=False, alpha=0.8)
    # beam.set_linestyle="dashed"
    # beam.set_edgecolor="gold"
    # beam.set_facecolor="gold"
    # beam.fill=False
    ax.add_artist(beam)
    ax.scatter(ra_offset, dec_offset)
    plt.axhline(0, color="k", ls="--")
    plt.axhline(med_dec_offset, color='r', ls="--")
    plt.axvline(0, color="k", ls="--")
    plt.axvline(med_ra_offset, color='r', ls="--")
    plt.title(title)
    plt.xlabel("RA (arcsec)")
    plt.ylabel("Dec (arcsec)")
    plt.xlim([-20,20])
    plt.ylim([-20,20])
    custom_lines=[Line2D([0], [0], color="r"),]
    ax.legend(custom_lines, ['Median Offset'])
    ax.text(10,-19, "Median RA Offset = {:.2f}\nMedian Dec Offset = {:.2f}".format(med_ra_offset, med_dec_offset))
    if save:
        logger.info("Plot saved")
        plt.savefig("sumss-offset.png", bbox_inches="tight")
    plt.close()
    
    
def source_counts(sumss_df, askap_df, crossmatch_df, max_sep, title="Source counts plot", save=True):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)
    ax.grid(zorder=1)
    num_sumss_sources=len(sumss_df.index)
    total_askap_sources = len(askap_df.index)
    askap_above_50 = askap_df[askap_df["dec"]>-50.0].reset_index(drop=True)
    askap_below_50 = askap_df[askap_df["dec"]<=-50.0].reset_index(drop=True)
    askap_above_50 = askap_above_50[askap_above_50["peak_flux"]>=0.010].reset_index(drop=True)
    askap_below_50 = askap_below_50[askap_below_50["peak_flux"]>=0.006].reset_index(drop=True)
    num_askap_above_50=len(askap_above_50.index)
    num_askap_below_50=len(askap_below_50.index)
    total_askap_expected=num_askap_below_50+num_askap_above_50
    num_sumss_sources_matched = len(crossmatch_df[crossmatch_df["d2d"]<=max_sep].index)
    logger.info("Number of ASKAP sources present expected to be seen:")
    logger.info("Dec > -50 deg (>= 10 mJy): {}".format(num_askap_above_50))
    logger.info("Dec <= -50 deg (>= 6 mJy): {}".format(num_askap_below_50))
    logger.info("Total: {}".format(total_askap_expected))
    logger.info("SUMSS sources with match <= {} arcsec: {}".format(max_sep, num_sumss_sources_matched))
    ax.bar((1,2,3,4),(total_askap_sources, total_askap_expected, num_sumss_sources, num_sumss_sources_matched), zorder=10, color=['C0', 'C0', 'C9', 'C9'])
    plt.xticks([1,2,3,4], ["Total ASKAP", "Expected ASKAP in SUMSS", "SUMSS Total", "SUMSS matched < {}\"".format(max_sep)])
    ax.set_ylabel("Number of Sources")
    for i,val in enumerate((total_askap_sources, total_askap_expected, num_sumss_sources, num_sumss_sources_matched)):
        ax.text((i+1-0.1), val+20, "{}".format(val),zorder=10)
    if save:
        logger.info("Plot saved")
        plt.savefig("askap-sumss-source-counts.png", bbox_inches="tight")
    plt.close()
    
    
def flux_ratios_askap_flux(df, max_sep, title="Flux ratio", save=True):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)
    # filter_df=df[df["d2d"]<=maxsep].reset_index(drop=True)
    # ratios=filter_df["askap_int_flux"]/(filter_df["sumss_St"]/1.e3)
    mask=[True if i < 5. else False for i in df["askap_sumss_int_flux_ratio"]]
    # ratios=ratios[mask]
    ax.scatter(df["askap_int_flux"][mask]*1000., df["askap_sumss_int_flux_ratio"][mask], label="SUMSS to ASKAP Crossmatch < {}\"".format(max_sep))
    median_flux_ratio=df["askap_sumss_int_flux_ratio"][mask].median()
    std_flux_ratio=df["askap_sumss_int_flux_ratio"][mask].std()
    ax.set_xlabel("log ASKAP Flux (mJy)")
    ax.set_ylabel("ASKAP / SUMSS Int. Flux Ratio")
    plt.title(title)
    ax.axhline(median_flux_ratio, label="Median Flux Ratio ({:.2f})".format(median_flux_ratio), color="red")
    ax.axhline(median_flux_ratio+std_flux_ratio, label="Median +/- STD (STD = {:.2f})".format(std_flux_ratio), color="gold")
    ax.axhline(median_flux_ratio-std_flux_ratio, color="gold")
    ax.set_xscale("log")
    plt.legend()
    if save:
        logger.info("Plot saved")
        plt.savefig("askap-sumss-flux-ratio-askap-flux.png", bbox_inches="tight")
    plt.close()
    
    
def flux_ratios_distance_from_centre(df, max_sep, title="Flux ratio", save=True):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)
    # filter_df=df[df["d2d"]<=maxsep].reset_index(drop=True)
    # ratios=filter_df["askap_int_flux"]/(filter_df["sumss_St"]/1.e3)
    mask=[True if i < 5. else False for i in df["askap_sumss_int_flux_ratio"]]
    # ratios=ratios[mask]
    ax.scatter(df["askap_distance_from_centre"][mask], df["askap_sumss_int_flux_ratio"][mask], label="SUMSS to ASKAP Crossmatch < {}\"".format(max_sep))
    median_flux_ratio=df["askap_sumss_int_flux_ratio"][mask].median()
    std_flux_ratio=df["askap_sumss_int_flux_ratio"][mask].std()
    ax.set_xlabel("ASKAP Position From Image Centre (deg)")
    ax.set_ylabel("ASKAP / SUMSS Int. Flux Ratio")
    plt.title(title)
    ax.axhline(median_flux_ratio, label="Median Flux Ratio ({:.2f})".format(median_flux_ratio), color="red")
    ax.axhline(median_flux_ratio+std_flux_ratio, label="Median +/- STD (STD = {:.2f})".format(std_flux_ratio), color="gold")
    ax.axhline(median_flux_ratio-std_flux_ratio, color="gold")
    plt.legend()
    if save:
        logger.info("Plot saved")
        plt.savefig("askap-sumss-flux-ratio-askap-image-position.png", bbox_inches="tight")
    plt.close()
    
    

