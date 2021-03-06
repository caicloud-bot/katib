import json

from django.test import TestCase

from suggestion.models import Study
from suggestion.algorithm.abstract_algorithm import AbstractSuggestionAlgorithm
from suggestion.algorithm.chocolate_bayes import ChocolateBayesAlgorithm


class ChocolateBayesAlgorithmTest(TestCase):
  def setUp(self):
    study_configuration_json = {
        "goal":
        "MAXIMIZE",
        "maxTrials":
        5,
        "maxParallelTrials":
        1,
        "randomInitTrials":
        1,
        "params": [{
            "parameterName": "l1_normalization",
            "type": "DOUBLE",
            "minValue": 0.01,
            "maxValue": 0.99,
            "scalingType": "LINEAR"
        }, {
            "parameterName": "learning_rate",
            "type": "DOUBLE",
            "minValue": 0.01,
            "maxValue": 0.5,
            "scalingType": "LINEAR"
        }, {
            "parameterName": "hidden2",
            "type": "DISCRETE",
            "feasiblePoints": "8, 16, 32, 64",
            "scalingType": "LINEAR"
        }, {
            "parameterName": "optimizer",
            "type": "CATEGORICAL",
            "feasiblePoints": "sgd, adagrad, adam, ftrl",
            "scalingType": "LINEAR"
        }]
    }
    study_configuration = json.dumps(study_configuration_json)
    self.study = Study.create("ChocolateBayesStudy", study_configuration)

  def tearDown(self):
    pass

  def test_init(self):
    instance = ChocolateBayesAlgorithm()

    self.assertTrue(isinstance(instance, AbstractSuggestionAlgorithm))

    self.assertEqual(instance.__class__, ChocolateBayesAlgorithm)

  def test_get_multiple_suggestions(self):
    instance = ChocolateBayesAlgorithm()

    new_trials = instance.get_new_suggestions(self.study.id, number=3)
    self.assertEqual(len(new_trials), 3)

  def test_get_new_suggestions(self):
    instance = ChocolateBayesAlgorithm()

    new_trials = instance.get_new_suggestions(self.study.id, number=3)
    self.assertEqual(len(new_trials), 3)

    new_trials = instance.get_new_suggestions(self.study.id, number=3)

    for new_trial in new_trials:
      new_parameter_values_json = json.loads(new_trial.parameter_values)

      self.assertTrue(
          0.99 >= new_parameter_values_json["l1_normalization"] >= 0.01)
      self.assertTrue(
          0.5 >= new_parameter_values_json["learning_rate"] >= 0.01)
      self.assertTrue(new_parameter_values_json["hidden2"] in [8, 16, 32, 64])
      self.assertTrue(new_parameter_values_json["optimizer"] in [
          "sgd", "adagrad", "adam", "ftrl"
      ])
