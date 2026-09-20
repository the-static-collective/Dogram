(* DOGWOLF-001: independent exact finite oracle for the frozen V4 path specimen.
   Run with wolframscript -file research/dogwolf_001.wl; optional, not a runtime dependency. *)
Module[{carrier, paths, composites, fibers, pairs, firstFailure, receipt},
 carrier = Tuples[{0, 1}, 2];
 paths = Tuples[carrier, 2];
 composites = Mod[Total[#], 2] & /@ paths;
 fibers = GatherBy[Range[Length[paths]], composites[[#]] &];
 pairs = Flatten[Subsets[#, {2}] & /@ fibers, 1];
 firstFailure = SelectFirst[pairs,
   paths[[#[[1]], 1]] =!= paths[[#[[2]], 1]] &,
   Missing["NotFound"]];
 receipt = <|
   "carrierSize" -> Length[carrier],
   "pathCount" -> Length[paths],
   "fiberSizes" -> (Length /@ fibers),
   "sameCompositeDistinctPathPairs" -> Length[pairs],
   "compositePreserved" -> AllTrue[pairs,
     composites[[#[[1]]]] === composites[[#[[2]]]] &],
   "firstArrowPreserved" -> (firstFailure === Missing["NotFound"]),
   "firstCounterexampleStatesOneBased" -> firstFailure,
   "firstCounterexampleSharedComposite" -> composites[[firstFailure[[1]]]],
   "firstCounterexampleArrows" -> paths[[firstFailure, 1]]
 |>;
 Print[ExportString[receipt, "RawJSON"]];
]
