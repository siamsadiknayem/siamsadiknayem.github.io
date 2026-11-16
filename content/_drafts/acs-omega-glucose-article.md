---
title: "Our article on non-invasive glucose monitoring in ACS Omega"
category: Publications
tags: [glucose monitoring, NIR spectroscopy, machine learning]
excerpt: >-
  A short summary of our ACS Omega paper on estimating blood glucose from
  near-infrared transmittance with machine learning.
---
<!--
DRAFT — written by Claude from the paper's abstract. Before publishing:
  1. Add one or two sentences on what YOU did in this study (not yet provided).
  2. Check the wording, then move this file to _posts/ and rename it
     YYYY-MM-DD-acs-omega-glucose-article.md (use today's date).
-->

Our article *Noninvasive Blood Glucose Monitoring with Machine Learning Enhanced Transmittance Spectroscopy* has been published in *ACS Omega* (vol. 11, issue 19, pp. 27931–27941). I am the second author, with Tanmoy Kumar Paul, Md Abdur Rakib, Md Jahirul Islam, Md Rejvi Kaysir and Shazzad Rassel.

## The question

Finger-prick glucometers are still the standard for people managing diabetes. They are reliable, but frequent pricking is uncomfortable, and that discourages the regular measurement good glucose control depends on. Could a low-cost optical measurement through the skin do the same job?

## What the study did

The study measured light transmitted through tissue at three wavelengths — 650, 808 and 940 nm. Simulations of light absorption in skin layers, together with in vitro experiments, identified 940 nm as the most suitable wavelength: sensitive to glucose, with little interference from water absorption.

An in vivo transmittance setup was then used to collect 200 measurements alongside clinical reference values, and several machine-learning models were trained to predict glucose concentration from the optical data.

## What we found

The best model, XGBoost, reached R² = 0.94 with a root-mean-squared error of 23.92 mg/dL. On the Clarke Error Grid — the standard clinical check for glucose meters — 92.5% of predictions fell in Zone A and the rest in Zone B, with none in the clinically risky Zones C–E.

## Where this goes next

This builds on the multispectral sensor from my undergraduate thesis, presented at IEEE QPAIN 2025. The open questions I am most interested in are making the measurement robust across different people and moving it towards a wearable form.

**Read the paper:** [doi.org/10.1021/acsomega.5c11682](https://doi.org/10.1021/acsomega.5c11682) (open access)
