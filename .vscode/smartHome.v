(* SmartHome.v *)

Inductive TimeOfDay :=
| Morning
| Afternoon
| Evening
| Night.

Inductive Motion :=
| MotionDetected
| NoMotion.

Inductive Temperature :=
| Cold
| Moderate
| Hot.

Inductive Action :=
| TurnOnLights
| TurnOffLights
| TurnOnAC
| TurnOffAC
| DoNothing.

Record HomeState := {
  time : TimeOfDay;
  motion : Motion;
  temp : Temperature
}.

(* Definition rule_lights (s : HomeState) : Action :=
  match s.time, s.motion with
  | Night, MotionDetected => TurnOnLights
  | _, _ => DoNothing
  end. *)
  Definition rule_lights (s : HomeState) : Action :=
  match time s, motion s with
  | Night, MotionDetected => TurnOnLights
  | _, _ => DoNothing
  end.
  Definition rule_lights_off (s : HomeState) : Action :=
  match time s, motion s with
  | Morning, NoMotion => TurnOffLights
  | Afternoon, NoMotion => TurnOffLights
  | _, _ => DoNothing
  end.

  Definition rule_temperature (s : HomeState) : Action :=
  match temp s with
  | Hot => TurnOnAC
  | Cold => TurnOffAC
  | Moderate => DoNothing
  end.
  Definition smart_home_reasoner (s : HomeState) : Action :=
  match rule_lights s with
  | DoNothing =>
      match rule_lights_off s with
      | DoNothing => rule_temperature s
      | act => act
      end
  | act => act
  end.


Definition test_state_1 : HomeState :=
  {| time := Night; motion := MotionDetected; temp := Moderate |}.



Eval compute in smart_home_reasoner test_state_1.


Definition test_state_2 : HomeState :=
  {| time := Morning; motion := NoMotion; temp := Moderate |}.

Eval compute in smart_home_reasoner test_state_2.


Definition test_state_3 : HomeState :=
  {| time := Afternoon; motion := MotionDetected; temp := Hot |}.

Eval compute in smart_home_reasoner test_state_3.

Definition t4 : HomeState :=
  {| time := Night; motion := NoMotion; temp := Cold |}.

Eval compute in smart_home_reasoner t4.