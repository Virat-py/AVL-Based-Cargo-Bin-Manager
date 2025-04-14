# AVL-Based-Cargo-Bin-Manager

Efficient cargo management is critical in interstellar logistics! This project implements a bin-packing system using **AVL Trees** for optimal cargo assignment based on different color-coded strategies.

> COL106 Assignment 2 – Data Structures

---

## 🌌 Overview

The **Galactic Cargo Management System (GCMS)** helps a space shipping company assign cargo to bins efficiently based on:

- **Bin ID** and **Remaining Capacity**
- **Cargo Color**, which determines the bin assignment strategy

### Cargo Colors and Placement Algorithms:

| Color  | Strategy           | Tie-Breaker     |
|--------|--------------------|-----------------|
| 🔵 Blue   | Compact Fit        | Least Bin ID    |
| 🟡 Yellow | Compact Fit        | Greatest Bin ID |
| 🔴 Red    | Largest Fit        | Least Bin ID    |
| 🟢 Green  | Largest Fit        | Greatest Bin ID |

---

## 🧠 Features

- AVL Trees ensure `O(log n)` performance for all major operations.
- Supports adding/removing bins and objects efficiently.
- Keeps track of bin capacity and object assignments.
- Handles exceptions when no suitable bin is found.


