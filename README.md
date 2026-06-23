# Policy Editor

A simple policy editor that allows users to preview the impact of proposed policy changes.

## Features

* Preview of proposed policy changes
* Simulated traffic graph
* Cancel or confirm rollout of proposed policy

## Usage

1. Create a `Policy` object with the current and proposed policies.
2. Create a `PolicyEditor` object with the `Policy` objects.
3. Use the `get_policy_diff` method to get a diff between the current and proposed policies.
4. Use the `simulate_traffic_graph` method to simulate a traffic graph based on the proposed policy.
5. Use the `confirm_rollout` or `cancel_rollout` methods to confirm or cancel the rollout of the proposed policy.
