(* DOGWOLF-002: independent exact oracle for a quotient path with no lift.
   Optional: wolframscript -file research/dogwolf_002.wl *)
Module[{cls, edges, projected, first, second, lifts, repaired, repairedLifts},
 cls = <|"p" -> "P", "qIn" -> "Q", "qOut" -> "Q", "r" -> "R"|>;
 edges = {{"p", "enter", "qIn"}, {"qOut", "exit", "r"}};
 projected = ({cls[#[[1]]], #[[2]], cls[#[[3]]]} & /@ edges);
 first = Select[edges, #[[1]] == "p" && #[[2]] == "enter" && cls[#[[3]]] == "Q" &];
 second = Select[edges, cls[#[[1]]] == "Q" && #[[2]] == "exit" && cls[#[[3]]] == "R" &];
 lifts = Select[Tuples[{first, second}], #[[1, 3]] === #[[2, 1]] &];
 repaired = Append[edges, {"qIn", "exit", "r"}];
 repairedLifts = Select[
   Tuples[{Select[repaired, #[[2]] == "enter" &], Select[repaired, #[[2]] == "exit" &]}],
   #[[1, 3]] === #[[2, 1]] &
 ];
 Print[ExportString[<|
    "quotientEdges" -> projected,
    "eachEdgeWitnessed" -> (Length[first] == 1 && Length[second] == 1),
    "concreteTwoStepWitnessCount" -> Length[lifts],
    "reachableAtJoin" -> first[[All, 3]],
    "neededExitSources" -> second[[All, 1]],
    "repairAddsConcreteLift" -> (Length[repairedLifts] > 0)
   |>, "RawJSON"]]
]
