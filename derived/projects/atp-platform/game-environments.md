<!-- prograph:generated -->

---
indexed_at: "2026-07-07T16:11:23Z"
kind: python
name: game-environments
parent: atp-platform
prograph: project
root: ./atp-platform/game-environments
snapshot: 1
---

# game-environments

> > Standalone game theory environments for evaluating AI agents in strategic interactions

## Manifest

- declared package: `game-environments` version `1.0.0`

## Public surface

### MCP tools exposed

_None._

### Contracts declared

_None._

### Public symbols

- `COOPERATIVE_ACTIONS` (const) — `game_envs/analysis/cooperation.py:14`
- `cooperation_rate` (function) — `game_envs/analysis/cooperation.py:56`
- `conditional_cooperation` (function) — `game_envs/analysis/cooperation.py:83`
- `reciprocity_index` (function) — `game_envs/analysis/cooperation.py:155`
- `compute_best_response` (function) — `game_envs/analysis/exploitability.py:150`
- `compute_exploitability` (function) — `game_envs/analysis/exploitability.py:179`
- `compute_exploitability_from_game` (function) — `game_envs/analysis/exploitability.py:245`
- `gini_coefficient` (function) — `game_envs/analysis/fairness.py:53`
- `envy_freeness` (function) — `game_envs/analysis/fairness.py:88`
- `proportionality` (function) — `game_envs/analysis/fairness.py:120`
- `utilitarian_welfare` (function) — `game_envs/analysis/fairness.py:174`
- `NashSolver` (class) — `game_envs/analysis/nash_solver.py:19`
- `PopulationDynamics` (class) — `game_envs/analysis/population.py:156`
- `ReplicatorDynamics` (class) — `game_envs/analysis/population.py:177`
- `MoranProcess` (class) — `game_envs/analysis/population.py:218`
- `is_ess` (function) — `game_envs/analysis/population.py:297`
- `PopulationSimulator` (class) — `game_envs/analysis/population.py:382`
- `ActionSpace` (class) — `game_envs/core/action.py:10`
- `DiscreteActionSpace` (class) — `game_envs/core/action.py:34`
- `ContinuousActionSpace` (class) — `game_envs/core/action.py:64`
- `StructuredActionSpace` (class) — `game_envs/core/action.py:107`
- `CommunicationMode` (class) — `game_envs/core/communication.py:12`
- `CommunicationChannel` (class) — `game_envs/core/communication.py:21`
- `ValidationError` (class) — `game_envs/core/errors.py:4`
- `GameType` (class) — `game_envs/core/game.py:21`
- `MoveOrder` (class) — `game_envs/core/game.py:30`
- `Game` (class) — `game_envs/core/game.py:86`
- `GameHistory` (class) — `game_envs/core/history.py:10`
- `Strategy` (class) — `game_envs/core/strategy.py:11`
- `AuctionType` (class) — `game_envs/games/auction.py:21`
- `ValueDistribution` (class) — `game_envs/games/auction.py:28`
- `A` (const) — `game_envs/games/battle_of_sexes.py:18`
- `B` (const) — `game_envs/games/battle_of_sexes.py:19`
- `MAX_SLOTS_PER_DAY` (const) — `game_envs/games/el_farol.py:60`
- `ElFarolActionSpace` (class) — `game_envs/games/el_farol.py:63`
- `COOPERATE` (const) — `game_envs/games/prisoners_dilemma.py:18`
- `DEFECT` (const) — `game_envs/games/prisoners_dilemma.py:19`
- `PGStage` (class) — `game_envs/games/public_goods.py:20`
- `GameRegistry` (class) — `game_envs/games/registry.py:11`
- `register_game` (function) — `game_envs/games/registry.py:189`
- `STAG` (const) — `game_envs/games/stag_hunt.py:18`
- `HARE` (const) — `game_envs/games/stag_hunt.py:19`
- `TruthfulBidder` (class) — `game_envs/strategies/auction_strategies.py:12`
- `ShadeBidder` (class) — `game_envs/strategies/auction_strategies.py:29`
- `RandomBidder` (class) — `game_envs/strategies/auction_strategies.py:57`
- `UniformAllocation` (class) — `game_envs/strategies/blotto_strategies.py:12`
- `ConcentratedAllocation` (class) — `game_envs/strategies/blotto_strategies.py:34`
- `NashMixed` (class) — `game_envs/strategies/blotto_strategies.py:64`
- `ACTION_A` (const) — `game_envs/strategies/bos_strategies.py:10`
- `ACTION_B` (const) — `game_envs/strategies/bos_strategies.py:11`
- `AlwaysA` (class) — `game_envs/strategies/bos_strategies.py:14`
- `AlwaysB` (class) — `game_envs/strategies/bos_strategies.py:25`
- `Alternating` (class) — `game_envs/strategies/bos_strategies.py:36`
- `SelfishRouter` (class) — `game_envs/strategies/congestion_strategies.py:12`
- `SocialOptimum` (class) — `game_envs/strategies/congestion_strategies.py:44`
- `EpsilonGreedy` (class) — `game_envs/strategies/congestion_strategies.py:76`
- `Traditionalist` (class) — `game_envs/strategies/el_farol_strategies.py:84`
- `TrendFollower` (class) — `game_envs/strategies/el_farol_strategies.py:118`
- `Contrarian` (class) — `game_envs/strategies/el_farol_strategies.py:147`
- `Gambler` (class) — `game_envs/strategies/el_farol_strategies.py:175`
- `SmartPredictor` (class) — `game_envs/strategies/el_farol_strategies.py:217`
- `Scout` (class) — `game_envs/strategies/el_farol_strategies.py:254`
- `COOPERATE` (const) — `game_envs/strategies/pd_strategies.py:11`
- `DEFECT` (const) — `game_envs/strategies/pd_strategies.py:12`
- `AlwaysCooperate` (class) — `game_envs/strategies/pd_strategies.py:15`
- `AlwaysDefect` (class) — `game_envs/strategies/pd_strategies.py:26`
- `TitForTat` (class) — `game_envs/strategies/pd_strategies.py:37`
- `GrimTrigger` (class) — `game_envs/strategies/pd_strategies.py:61`
- `Pavlov` (class) — `game_envs/strategies/pd_strategies.py:89`
- `RandomStrategy` (class) — `game_envs/strategies/pd_strategies.py:120`
- `FullContributor` (class) — `game_envs/strategies/pg_strategies.py:11`
- `FreeRider` (class) — `game_envs/strategies/pg_strategies.py:26`
- `ConditionalCooperator` (class) — `game_envs/strategies/pg_strategies.py:41`
- `Punisher` (class) — `game_envs/strategies/pg_strategies.py:72`
- `StrategyRegistry` (class) — `game_envs/strategies/registry.py:10`
- `STAG` (const) — `game_envs/strategies/stag_hunt_strategies.py:10`
- `HARE` (const) — `game_envs/strategies/stag_hunt_strategies.py:11`
- `AlwaysStag` (class) — `game_envs/strategies/stag_hunt_strategies.py:14`
- `AlwaysHare` (class) — `game_envs/strategies/stag_hunt_strategies.py:25`
- `StagTitForTat` (class) — `game_envs/strategies/stag_hunt_strategies.py:36`
- `StubGame` (class) — `tests/conftest.py:31`
- `StubStrategy` (class) — `tests/conftest.py:117`
- `TestDiscreteActionSpace` (class) — `tests/test_action.py:16`
- `TestContinuousActionSpace` (class) — `tests/test_action.py:73`
- `TestStructuredActionSpace` (class) — `tests/test_action.py:138`
- `TestDiscreteActionSpaceProperties` (class) — `tests/test_action_properties.py:17`
- `TestContinuousActionSpaceProperties` (class) — `tests/test_action_properties.py:85`
- `TestStructuredActionSpaceProperties` (class) — `tests/test_action_properties.py:164`
- `TestAuctionConfig` (class) — `tests/test_auction.py:18`
- `TestAuctionProperties` (class) — `tests/test_auction.py:81`
- `TestAuctionReset` (class) — `tests/test_auction.py:137`
- `TestAuctionFirstPrice` (class) — `tests/test_auction.py:224`
- `TestAuctionSecondPrice` (class) — `tests/test_auction.py:273`
- `TestAuctionFirstPriceOptimalShading` (class) — `tests/test_auction.py:397`
- `TestAuctionReservePrice` (class) — `tests/test_auction.py:452`
- `TestAuctionTies` (class) — `tests/test_auction.py:501`
- `TestAuctionObserve` (class) — `tests/test_auction.py:539`
- `TestAuctionToPrompt` (class) — `tests/test_auction.py:629`
- `TestAuctionRepeated` (class) — `tests/test_auction.py:676`
- `TestAuctionRegistry` (class) — `tests/test_auction.py:756`
- `TestBoSConfig` (class) — `tests/test_battle_of_sexes.py:11`
- `TestBattleOfSexesPayoffs` (class) — `tests/test_battle_of_sexes.py:25`
- `TestBattleOfSexesRepeated` (class) — `tests/test_battle_of_sexes.py:67`
- `TestBattleOfSexesRegistry` (class) — `tests/test_battle_of_sexes.py:89`
- `test_validate_action_accepts_a` (function) — `tests/test_battle_of_sexes_service_methods.py:19`
- `test_validate_action_accepts_b` (function) — `tests/test_battle_of_sexes_service_methods.py:23`
- `test_validate_action_rejects_unknown_choice` (function) — `tests/test_battle_of_sexes_service_methods.py:27`
- `test_validate_action_rejects_missing_choice` (function) — `tests/test_battle_of_sexes_service_methods.py:32`
- `test_validate_action_rejects_non_dict` (function) — `tests/test_battle_of_sexes_service_methods.py:37`
- `test_default_action_on_timeout_is_a` (function) — `tests/test_battle_of_sexes_service_methods.py:42`
- `test_format_state_empty_history_exposes_your_preferred` (function) — `tests/test_battle_of_sexes_service_methods.py:47`
- `test_format_state_populated_history_from_both_sides` (function) — `tests/test_battle_of_sexes_service_methods.py:68`
- `test_compute_round_payoffs_coord_on_a` (function) — `tests/test_battle_of_sexes_service_methods.py:85`
- `test_compute_round_payoffs_coord_on_b` (function) — `tests/test_battle_of_sexes_service_methods.py:92`
- `test_compute_round_payoffs_mismatch_ab` (function) — `tests/test_battle_of_sexes_service_methods.py:99`
- `test_compute_round_payoffs_mismatch_ba` (function) — `tests/test_battle_of_sexes_service_methods.py:105`
- `TestBlottoConfig` (class) — `tests/test_colonel_blotto.py:14`
- `TestColonelBlottoProperties` (class) — `tests/test_colonel_blotto.py:62`
- `TestAllocationValidation` (class) — `tests/test_colonel_blotto.py:108`
- `TestPayoffComputation` (class) — `tests/test_colonel_blotto.py:209`
- `TestColonelBlottoRepeated` (class) — `tests/test_colonel_blotto.py:356`
- `TestColonelBlottoObserve` (class) — `tests/test_colonel_blotto.py:492`
- `TestToPrompt` (class) — `tests/test_colonel_blotto.py:553`
- `TestNoPureNashEquilibrium` (class) — `tests/test_colonel_blotto.py:592`
- `TestColonelBlottoRegistry` (class) — `tests/test_colonel_blotto.py:734`
- `TestCommunicationMode` (class) — `tests/test_communication.py:19`
- `TestCommunicationChannelNoComm` (class) — `tests/test_communication.py:33`
- `TestCommunicationChannelPreAction` (class) — `tests/test_communication.py:54`
- `TestCommunicationChannelPostAction` (class) — `tests/test_communication.py:122`
- `TestCommunicationChannelFree` (class) — `tests/test_communication.py:145`
- `TestCommunicationChannelSerialization` (class) — `tests/test_communication.py:165`
- `TestInformationSet` (class) — `tests/test_communication.py:213`
- `TestGameConfigCommunication` (class) — `tests/test_communication.py:304`
- `TestGameCommunication` (class) — `tests/test_communication.py:334`
- `TestPDWithCommunication` (class) — `tests/test_communication.py:363`
- `TestAuctionWithInformationSet` (class) — `tests/test_communication.py:449`
- `TestMessageTimestamp` (class) — `tests/test_communication.py:551`
- `TestInformationSetFilterHistory` (class) — `tests/test_communication.py:585`
- `TestGameGetInformationSet` (class) — `tests/test_communication.py:693`
- `TestResetClearsChannel` (class) — `tests/test_communication.py:736`
- `TestPDPostActionCommunication` (class) — `tests/test_communication.py:803`
- `TestRouteDefinition` (class) — `tests/test_congestion.py:18`
- `TestCongestionConfig` (class) — `tests/test_congestion.py:46`
- `TestCongestionGameProperties` (class) — `tests/test_congestion.py:91`
- `TestCongestionGameLatency` (class) — `tests/test_congestion.py:140`
- `TestCongestionGameOneShot` (class) — `tests/test_congestion.py:162`
- `TestCongestionGameNPlayer` (class) — `tests/test_congestion.py:228`
- `TestCongestionGameNashFlow` (class) — `tests/test_congestion.py:289`
- `TestBraessParadox` (class) — `tests/test_congestion.py:341`
- `TestCongestionGameRepeated` (class) — `tests/test_congestion.py:489`
- `TestCongestionGameObserve` (class) — `tests/test_congestion.py:573`
- `TestCongestionGameRegistry` (class) — `tests/test_congestion.py:641`
- `TestCongestionGameToPrompt` (class) — `tests/test_congestion.py:665`
- `TestBraessParadoxVerification` (class) — `tests/test_congestion.py:723`
- `TestCooperationRate` (class) — `tests/test_cooperation.py:67`
- `TestConditionalCooperation` (class) — `tests/test_cooperation.py:107`
- `TestReciprocityIndex` (class) — `tests/test_cooperation.py:154`
- `TestCooperationMetricsSerialization` (class) — `tests/test_cooperation.py:204`
- `TestCooperationIntegration` (class) — `tests/test_cooperation.py:240`
- `test_validate_action_accepts_intervals` (function) — `tests/test_el_farol.py:22`
- `test_validate_action_orders_intervals` (function) — `tests/test_el_farol.py:27`
- `test_validate_action_accepts_empty_list` (function) — `tests/test_el_farol.py:35`
- `test_validate_action_rejects_overlapping_intervals` (function) — `tests/test_el_farol.py:40`
- `test_validate_action_rejects_adjacent_intervals` (function) — `tests/test_el_farol.py:46`
- `test_validate_action_rejects_out_of_range` (function) — `tests/test_el_farol.py:52`
- `test_validate_action_rejects_negative` (function) — `tests/test_el_farol.py:58`
- `test_validate_action_rejects_too_many_total_slots` (function) — `tests/test_el_farol.py:64`
- `test_validate_action_rejects_too_many_intervals` (function) — `tests/test_el_farol.py:71`
- `test_validate_action_rejects_non_list_intervals` (function) — `tests/test_el_farol.py:78`
- `test_validate_action_rejects_missing_intervals_key` (function) — `tests/test_el_farol.py:84`
- `test_validate_action_rejects_legacy_slots_key` (function) — `tests/test_el_farol.py:90`
- `test_validate_action_rejects_non_dict` (function) — `tests/test_el_farol.py:96`
- `test_validate_action_rejects_bool_bounds` (function) — `tests/test_el_farol.py:102`
- `test_validate_action_rejects_bad_pair_shape` (function) — `tests/test_el_farol.py:108`
- `test_validate_action_rejects_start_after_end` (function) — `tests/test_el_farol.py:114`
- `test_default_action_on_timeout_returns_empty_intervals` (function) — `tests/test_el_farol.py:120`
- `test_format_state_empty_history` (function) — `tests/test_el_farol.py:125`
- `test_format_state_populated_history_aggregates_attendance` (function) — `tests/test_el_farol.py:151`
- `test_compute_round_payoffs_legacy_mode_happy_minus_crowded` (function) — `tests/test_el_farol.py:184`
- `test_format_state_your_history_is_defensive_copy` (function) — `tests/test_el_farol.py:207`
- `test_scoring_mode_validation_rejects_unknown` (function) — `tests/test_el_farol.py:231`
- `test_scoring_mode_default_is_happy_only` (function) — `tests/test_el_farol.py:237`
- `test_scoring_mode_dataclass_round_trip` (function) — `tests/test_el_farol.py:244`
- `test_compute_round_payoffs_happy_only_default` (function) — `tests/test_el_farol.py:257`
- `test_step_happy_only_accumulates_t_happy_and_t_crowded` (function) — `tests/test_el_farol.py:285`
- `test_get_payoffs_happy_only_returns_t_happy_sum` (function) — `tests/test_el_farol.py:319`
- `test_get_payoffs_happy_only_disqualification_still_applies` (function) — `tests/test_el_farol.py:345`
- `test_happy_only_per_round_payoff_is_non_negative` (function) — `tests/test_el_farol.py:368`
- `test_observation_includes_t_crowded_in_both_modes` (function) — `tests/test_el_farol.py:398`
- `test_to_prompt_happy_only_describes_no_penalty` (function) — `tests/test_el_farol.py:417`
- `test_to_prompt_legacy_describes_ratio_formula` (function) — `tests/test_el_farol.py:440`
- `test_get_payoffs_legacy_mode_returns_ratio` (function) — `tests/test_el_farol.py:457`
- `PD_P1` (const) — `tests/test_exploitability.py:28`
- `PD_P2` (const) — `tests/test_exploitability.py:29`
- `TestEmpiricalStrategy` (class) — `tests/test_exploitability.py:32`
- `TestExploitabilityResult` (class) — `tests/test_exploitability.py:105`
- `TestBestResponse` (class) — `tests/test_exploitability.py:120`
- `TestComputeExploitability` (class) — `tests/test_exploitability.py:168`
- `TestComputeExploitabilityFromGame` (class) — `tests/test_exploitability.py:281`
- `TestCrossSolverExploitability` (class) — `tests/test_exploitability.py:362`
- `TestGiniCoefficient` (class) — `tests/test_fairness.py:18`
- `TestEnvyFreeness` (class) — `tests/test_fairness.py:60`
- `TestProportionality` (class) — `tests/test_fairness.py:92`
- `TestUtilitarianWelfare` (class) — `tests/test_fairness.py:131`
- `TestFairnessMetricsSerialization` (class) — `tests/test_fairness.py:152`
- `TestGameConfig` (class) — `tests/test_game.py:10`
- `TestGameType` (class) — `tests/test_game.py:73`
- `TestMoveOrder` (class) — `tests/test_game.py:81`
- `TestStubGame` (class) — `tests/test_game.py:87`
- `TestGameHistory` (class) — `tests/test_history.py:9`
- `PD_P1` (const) — `tests/test_nash_solver.py:25`
- `PD_P2` (const) — `tests/test_nash_solver.py:26`
- `MP_P1` (const) — `tests/test_nash_solver.py:29`
- `MP_P2` (const) — `tests/test_nash_solver.py:30`
- `BOS_P1` (const) — `tests/test_nash_solver.py:33`
- `BOS_P2` (const) — `tests/test_nash_solver.py:34`
- `RPS_P1` (const) — `tests/test_nash_solver.py:37`
- `RPS_P2` (const) — `tests/test_nash_solver.py:44`
- `TestNashEquilibriumModel` (class) — `tests/test_nash_solver.py:47`
- `TestSupportEnumeration` (class) — `tests/test_nash_solver.py:133`
- `TestLemkeHowson` (class) — `tests/test_nash_solver.py:216`
- `TestFictitiousPlay` (class) — `tests/test_nash_solver.py:285`
- `TestReplicatorDynamics` (class) — `tests/test_nash_solver.py:343`
- `TestSolve2Player` (class) — `tests/test_nash_solver.py:407`
- `TestSolveNPlayer` (class) — `tests/test_nash_solver.py:435`
- `TestPerformance` (class) — `tests/test_nash_solver.py:460`
- `TestVerificationOnKnownGames` (class) — `tests/test_nash_solver.py:502`
- `PD_PAYOFF` (const) — `tests/test_population.py:25`
- `TestPopulationSnapshot` (class) — `tests/test_population.py:36`
- `TestPopulationResult` (class) — `tests/test_population.py:62`
- `TestReplicatorDynamics` (class) — `tests/test_population.py:116`
- `TestMoranProcess` (class) — `tests/test_population.py:186`
- `TestIsESS` (class) — `tests/test_population.py:240`
- `TestPopulationSimulator` (class) — `tests/test_population.py:289`
- `TestPDConfig` (class) — `tests/test_prisoners_dilemma.py:16`
- `TestPrisonersDilemmaOneShot` (class) — `tests/test_prisoners_dilemma.py:74`
- `TestPrisonersDilemmaRepeated` (class) — `tests/test_prisoners_dilemma.py:164`
- `TestPrisonersDilemmaNoise` (class) — `tests/test_prisoners_dilemma.py:252`
- `TestPrisonersDilemmaObserve` (class) — `tests/test_prisoners_dilemma.py:306`
- `TestPrisonersDilemmaSerialization` (class) — `tests/test_prisoners_dilemma.py:363`
- `TestPrisonersDilemmaValidateAction` (class) — `tests/test_prisoners_dilemma.py:393`
- `test_default_action_on_timeout_returns_defect` (function) — `tests/test_prisoners_dilemma.py:426`
- `test_format_state_accepts_generic_action_history_shape` (function) — `tests/test_prisoners_dilemma.py:431`
- `test_compute_round_payoffs_from_action_dicts` (function) — `tests/test_prisoners_dilemma.py:452`
- `test_format_state_empty_history` (function) — `tests/test_prisoners_dilemma.py:460`
- `TestPGConfig` (class) — `tests/test_public_goods.py:14`
- `TestPublicGoodsGameProperties` (class) — `tests/test_public_goods.py:76`
- `TestPublicGoodsGameOneShot` (class) — `tests/test_public_goods.py:159`
- `TestPublicGoodsGameNPlayer` (class) — `tests/test_public_goods.py:268`
- `TestPublicGoodsGameRepeated` (class) — `tests/test_public_goods.py:330`
- `TestPublicGoodsGamePunishment` (class) — `tests/test_public_goods.py:413`
- `TestPublicGoodsGameObserve` (class) — `tests/test_public_goods.py:513`
- `TestPublicGoodsGameRegistry` (class) — `tests/test_public_goods.py:627`
- `test_validate_action_accepts_float` (function) — `tests/test_public_goods_service_methods.py:22`
- `test_validate_action_coerces_int_to_float` (function) — `tests/test_public_goods_service_methods.py:26`
- `test_validate_action_accepts_zero` (function) — `tests/test_public_goods_service_methods.py:30`
- `test_validate_action_accepts_full_endowment` (function) — `tests/test_public_goods_service_methods.py:34`
- `test_validate_action_rejects_negative` (function) — `tests/test_public_goods_service_methods.py:40`
- `test_validate_action_rejects_above_endowment` (function) — `tests/test_public_goods_service_methods.py:45`
- `test_validate_action_rejects_non_number` (function) — `tests/test_public_goods_service_methods.py:50`
- `test_validate_action_rejects_bool` (function) — `tests/test_public_goods_service_methods.py:55`
- `test_validate_action_rejects_missing_field` (function) — `tests/test_public_goods_service_methods.py:62`
- `test_validate_action_rejects_non_dict` (function) — `tests/test_public_goods_service_methods.py:67`
- `test_default_action_on_timeout_is_zero_contribution` (function) — `tests/test_public_goods_service_methods.py:75`
- `test_compute_round_payoffs_all_contribute_full` (function) — `tests/test_public_goods_service_methods.py:82`
- `test_compute_round_payoffs_all_free_ride` (function) — `tests/test_public_goods_service_methods.py:93`
- `test_compute_round_payoffs_asymmetric` (function) — `tests/test_public_goods_service_methods.py:101`
- `test_compute_round_payoffs_missing_action_treated_as_zero` (function) — `tests/test_public_goods_service_methods.py:119`
- `test_format_state_empty_history` (function) — `tests/test_public_goods_service_methods.py:136`
- `test_format_state_exposes_full_contribution_vector` (function) — `tests/test_public_goods_service_methods.py:160`
- `TestGameRegistry` (class) — `tests/test_registry.py:79`
- `TestGameInfo` (class) — `tests/test_registry.py:217`
- `TestRegisterGameDecorator` (class) — `tests/test_registry.py:304`
- `TestBuiltinRegistration` (class) — `tests/test_registry.py:384`
- `TestSHConfig` (class) — `tests/test_stag_hunt.py:11`
- `TestStagHuntPayoffs` (class) — `tests/test_stag_hunt.py:37`
- `TestStagHuntNashEquilibria` (class) — `tests/test_stag_hunt.py:80`
- `TestStagHuntRepeated` (class) — `tests/test_stag_hunt.py:92`
- `TestStagHuntRegistry` (class) — `tests/test_stag_hunt.py:122`
- `test_validate_action_accepts_stag` (function) — `tests/test_stag_hunt_service_methods.py:19`
- `test_validate_action_accepts_hare` (function) — `tests/test_stag_hunt_service_methods.py:23`
- `test_validate_action_rejects_unknown_choice` (function) — `tests/test_stag_hunt_service_methods.py:27`
- `test_validate_action_rejects_missing_choice` (function) — `tests/test_stag_hunt_service_methods.py:32`
- `test_validate_action_rejects_non_dict` (function) — `tests/test_stag_hunt_service_methods.py:37`
- `test_default_action_on_timeout_is_hare` (function) — `tests/test_stag_hunt_service_methods.py:42`
- `test_format_state_empty_history` (function) — `tests/test_stag_hunt_service_methods.py:47`
- `test_format_state_populated_history_from_both_sides` (function) — `tests/test_stag_hunt_service_methods.py:65`
- `test_compute_round_payoffs_mutual_stag` (function) — `tests/test_stag_hunt_service_methods.py:97`
- `test_compute_round_payoffs_mutual_hare` (function) — `tests/test_stag_hunt_service_methods.py:104`
- `test_compute_round_payoffs_sucker_and_hare` (function) — `tests/test_stag_hunt_service_methods.py:111`
- `TestMessage` (class) — `tests/test_state.py:14`
- `TestRoundResult` (class) — `tests/test_state.py:40`
- `TestGameState` (class) — `tests/test_state.py:77`
- `TestObservation` (class) — `tests/test_state.py:123`
- `TestStepResult` (class) — `tests/test_state.py:189`
- `TestTruthfulBidder` (class) — `tests/test_strategies/test_auction_strategies.py:43`
- `TestShadeBidder` (class) — `tests/test_strategies/test_auction_strategies.py:58`
- `TestRandomBidder` (class) — `tests/test_strategies/test_auction_strategies.py:90`
- `TestAuctionIntegration` (class) — `tests/test_strategies/test_auction_strategies.py:109`
- `FIELDS` (const) — `tests/test_strategies/test_blotto_strategies.py:15`
- `TOTAL` (const) — `tests/test_strategies/test_blotto_strategies.py:16`
- `TestUniformAllocation` (class) — `tests/test_strategies/test_blotto_strategies.py:44`
- `TestConcentratedAllocation` (class) — `tests/test_strategies/test_blotto_strategies.py:67`
- `TestNashMixed` (class) — `tests/test_strategies/test_blotto_strategies.py:100`
- `TestBlottoIntegration` (class) — `tests/test_strategies/test_blotto_strategies.py:139`
- `TestSelfishRouter` (class) — `tests/test_strategies/test_congestion_strategies.py:45`
- `TestSocialOptimum` (class) — `tests/test_strategies/test_congestion_strategies.py:73`
- `TestEpsilonGreedy` (class) — `tests/test_strategies/test_congestion_strategies.py:108`
- `TestCongestionIntegration` (class) — `tests/test_strategies/test_congestion_strategies.py:156`
- `TestAlwaysCooperate` (class) — `tests/test_strategies/test_pd_strategies.py:58`
- `TestAlwaysDefect` (class) — `tests/test_strategies/test_pd_strategies.py:72`
- `TestTitForTat` (class) — `tests/test_strategies/test_pd_strategies.py:86`
- `TestGrimTrigger` (class) — `tests/test_strategies/test_pd_strategies.py:138`
- `TestPavlov` (class) — `tests/test_strategies/test_pd_strategies.py:176`
- `TestRandomStrategy` (class) — `tests/test_strategies/test_pd_strategies.py:205`
- `TestPDPayoffsMatchTheory` (class) — `tests/test_strategies/test_pd_strategies.py:224`
- `TestFullContributor` (class) — `tests/test_strategies/test_pg_strategies.py:49`
- `TestFreeRider` (class) — `tests/test_strategies/test_pg_strategies.py:64`
- `TestConditionalCooperator` (class) — `tests/test_strategies/test_pg_strategies.py:73`
- `TestPunisher` (class) — `tests/test_strategies/test_pg_strategies.py:129`
- `TestPGIntegration` (class) — `tests/test_strategies/test_pg_strategies.py:172`
- `TestStrategyRegistry` (class) — `tests/test_strategies/test_registry.py:11`
- `TestStubStrategy` (class) — `tests/test_strategy.py:32`
- `ALL_STRATEGIES` (const) — `tests/test_strategy.py:70`
- `TestAllStrategiesABC` (class) — `tests/test_strategy.py:93`
- `TestResetClearsState` (class) — `tests/test_strategy.py:122`

## Modules

_69 files, 326 public symbols, 0 internal imports._

- `game_envs/__init__.py` (python)
- `game_envs/analysis/__init__.py` (python)
- `game_envs/analysis/cooperation.py` (python)
- `game_envs/analysis/exploitability.py` (python)
- `game_envs/analysis/fairness.py` (python)
- `game_envs/analysis/models.py` (python)
- `game_envs/analysis/nash_solver.py` (python)
- `game_envs/analysis/population.py` (python)
- `game_envs/core/__init__.py` (python)
- `game_envs/core/action.py` (python)
- `game_envs/core/communication.py` (python)
- `game_envs/core/errors.py` (python)
- `game_envs/core/game.py` (python)
- `game_envs/core/history.py` (python)
- `game_envs/core/state.py` (python)
- `game_envs/core/strategy.py` (python)
- `game_envs/games/__init__.py` (python)
- `game_envs/games/auction.py` (python)
- `game_envs/games/battle_of_sexes.py` (python)
- `game_envs/games/colonel_blotto.py` (python)
- `game_envs/games/congestion.py` (python)
- `game_envs/games/el_farol.py` (python)
- `game_envs/games/prisoners_dilemma.py` (python)
- `game_envs/games/public_goods.py` (python)
- `game_envs/games/registry.py` (python)
- `game_envs/games/stag_hunt.py` (python)
- `game_envs/strategies/__init__.py` (python)
- `game_envs/strategies/auction_strategies.py` (python)
- `game_envs/strategies/blotto_strategies.py` (python)
- `game_envs/strategies/bos_strategies.py` (python)
- `game_envs/strategies/congestion_strategies.py` (python)
- `game_envs/strategies/el_farol_strategies.py` (python)
- `game_envs/strategies/pd_strategies.py` (python)
- `game_envs/strategies/pg_strategies.py` (python)
- `game_envs/strategies/registry.py` (python)
- `game_envs/strategies/stag_hunt_strategies.py` (python)
- `tests/__init__.py` (python)
- `tests/conftest.py` (python)
- `tests/test_action.py` (python)
- `tests/test_action_properties.py` (python)
- `tests/test_auction.py` (python)
- `tests/test_battle_of_sexes.py` (python)
- `tests/test_battle_of_sexes_service_methods.py` (python)
- `tests/test_colonel_blotto.py` (python)
- `tests/test_communication.py` (python)
- `tests/test_congestion.py` (python)
- `tests/test_cooperation.py` (python)
- `tests/test_el_farol.py` (python)
- `tests/test_exploitability.py` (python)
- `tests/test_fairness.py` (python)
- `tests/test_game.py` (python)
- `tests/test_history.py` (python)
- `tests/test_nash_solver.py` (python)
- `tests/test_population.py` (python)
- `tests/test_prisoners_dilemma.py` (python)
- `tests/test_public_goods.py` (python)
- `tests/test_public_goods_service_methods.py` (python)
- `tests/test_registry.py` (python)
- `tests/test_stag_hunt.py` (python)
- `tests/test_stag_hunt_service_methods.py` (python)
- `tests/test_state.py` (python)
- `tests/test_strategies/__init__.py` (python)
- `tests/test_strategies/test_auction_strategies.py` (python)
- `tests/test_strategies/test_blotto_strategies.py` (python)
- `tests/test_strategies/test_congestion_strategies.py` (python)
- `tests/test_strategies/test_pd_strategies.py` (python)
- `tests/test_strategies/test_pg_strategies.py` (python)
- `tests/test_strategies/test_registry.py` (python)
- `tests/test_strategy.py` (python)

## Inbound references

_None._

## Outbound references

_None._

## Outbound edges

_None._

## Inbound edges

- ← [[atp-dashboard]] · `package_dep` · `game-environments`
- ← [[atp-games]] · `package_dep` · `game-environments`
- ← [[atp-platform]] · `package_dep` · `game-environments`

## Recent changes (last 5)

- snapshot 1 (2026-07-07T16:11:23Z): project added (added)

## Drift findings

_None._
