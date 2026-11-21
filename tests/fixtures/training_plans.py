import pytest
from models.models import (
    TrainingPlan,
    TrainingUnit,
    TrainingExercise,
    TrainingExerciseSet,
)


@pytest.fixture()
def test_training_plan_first_user_1(
    db_session,
    test_first_user,
    test_exercise_first_user_1,
    test_exercise_first_user_2,
    test_exercise_first_user_3,
):
    training_plan = TrainingPlan(
        name="PPL",
        description="Push Pull Legs, 3 trainings per week",
        user_id=test_first_user.id,
        source="user",
    )

    db_session.add(training_plan)
    db_session.flush()
    db_session.refresh(training_plan)

    training_unit_1 = TrainingUnit(
        training_plan_id=training_plan.id,
        name="Push",
        description="Push - chest and triceps",
        unit_order=1,
    )
    training_unit_2 = TrainingUnit(
        training_plan_id=training_plan.id,
        name="Pull",
        description="Pull - lats and biceps",
        unit_order=2,
    )
    training_unit_3 = TrainingUnit(
        training_plan_id=training_plan.id,
        name="Legs",
        description="Legs - quads, glutes and hamstrings",
        unit_order=3,
    )

    db_session.add(training_unit_1)
    db_session.add(training_unit_2)
    db_session.add(training_unit_3)
    db_session.flush()
    db_session.refresh(training_unit_1)
    db_session.refresh(training_unit_2)
    db_session.refresh(training_unit_3)

    training_unit_1_training_exercise_1 = TrainingExercise(
        training_unit_id=training_unit_1.id,
        exercise_id=test_exercise_first_user_1.id,
        exercise_order=1,
    )
    training_unit_1_training_exercise_2 = TrainingExercise(
        training_unit_id=training_unit_1.id,
        exercise_id=test_exercise_first_user_2.id,
        exercise_order=2,
    )

    db_session.add(training_unit_1_training_exercise_1)
    db_session.add(training_unit_1_training_exercise_2)
    db_session.flush()
    db_session.refresh(training_unit_1_training_exercise_1)
    db_session.refresh(training_unit_1_training_exercise_2)

    training_unit_2_training_exercise_1 = TrainingExercise(
        training_unit_id=training_unit_2.id,
        exercise_id=test_exercise_first_user_2.id,
        exercise_order=1,
    )
    training_unit_2_training_exercise_2 = TrainingExercise(
        training_unit_id=training_unit_2.id,
        exercise_id=test_exercise_first_user_3.id,
        exercise_order=2,
    )

    db_session.add(training_unit_2_training_exercise_1)
    db_session.add(training_unit_2_training_exercise_2)
    db_session.flush()
    db_session.refresh(training_unit_2_training_exercise_1)
    db_session.refresh(training_unit_2_training_exercise_2)

    training_unit_3_training_exercise_1 = TrainingExercise(
        training_unit_id=training_unit_3.id,
        exercise_id=test_exercise_first_user_3.id,
        exercise_order=1,
    )

    db_session.add(training_unit_3_training_exercise_1)
    db_session.flush()
    db_session.refresh(training_unit_3_training_exercise_1)

    training_unit_1_training_exercise_1_set_1 = TrainingExerciseSet(
        training_exercise_id=training_unit_1_training_exercise_1.id,
        set_order=1,
        repetitions=10,
    )
    training_unit_1_training_exercise_1_set_2 = TrainingExerciseSet(
        training_exercise_id=training_unit_1_training_exercise_1.id,
        set_order=2,
        repetitions=8,
    )

    db_session.add(training_unit_1_training_exercise_1_set_1)
    db_session.add(training_unit_1_training_exercise_1_set_2)

    training_unit_1_training_exercise_2_set_1 = TrainingExerciseSet(
        training_exercise_id=training_unit_1_training_exercise_2.id,
        set_order=1,
        repetitions=12,
    )
    training_unit_1_training_exercise_2_set_2 = TrainingExerciseSet(
        training_exercise_id=training_unit_1_training_exercise_2.id,
        set_order=2,
        repetitions=12,
    )

    db_session.add(training_unit_1_training_exercise_2_set_1)
    db_session.add(training_unit_1_training_exercise_2_set_2)

    training_unit_2_training_exercise_1_set_1 = TrainingExerciseSet(
        training_exercise_id=training_unit_2_training_exercise_1.id,
        set_order=1,
        repetitions=6,
    )
    training_unit_2_training_exercise_1_set_2 = TrainingExerciseSet(
        training_exercise_id=training_unit_2_training_exercise_1.id,
        set_order=2,
        repetitions=6,
    )
    training_unit_2_training_exercise_1_set_3 = TrainingExerciseSet(
        training_exercise_id=training_unit_2_training_exercise_1.id,
        set_order=3,
        repetitions=6,
    )

    db_session.add(training_unit_2_training_exercise_1_set_1)
    db_session.add(training_unit_2_training_exercise_1_set_2)
    db_session.add(training_unit_2_training_exercise_1_set_3)

    training_unit_2_training_exercise_2_set_1 = TrainingExerciseSet(
        training_exercise_id=training_unit_2_training_exercise_2.id,
        set_order=1,
        repetitions=8,
    )
    training_unit_2_training_exercise_2_set_2 = TrainingExerciseSet(
        training_exercise_id=training_unit_2_training_exercise_2.id,
        set_order=2,
        repetitions=8,
    )
    training_unit_2_training_exercise_2_set_3 = TrainingExerciseSet(
        training_exercise_id=training_unit_2_training_exercise_2.id,
        set_order=3,
        repetitions=8,
    )

    db_session.add(training_unit_2_training_exercise_2_set_1)
    db_session.add(training_unit_2_training_exercise_2_set_2)
    db_session.add(training_unit_2_training_exercise_2_set_3)

    training_unit_3_training_exercise_1_set_1 = TrainingExerciseSet(
        training_exercise_id=training_unit_3_training_exercise_1.id,
        set_order=1,
        repetitions=10,
    )
    training_unit_3_training_exercise_1_set_2 = TrainingExerciseSet(
        training_exercise_id=training_unit_3_training_exercise_1.id,
        set_order=2,
        repetitions=9,
    )
    training_unit_3_training_exercise_1_set_3 = TrainingExerciseSet(
        training_exercise_id=training_unit_3_training_exercise_1.id,
        set_order=3,
        repetitions=8,
    )

    db_session.add(training_unit_3_training_exercise_1_set_1)
    db_session.add(training_unit_3_training_exercise_1_set_2)
    db_session.add(training_unit_3_training_exercise_1_set_3)
    db_session.commit()

    return training_plan
