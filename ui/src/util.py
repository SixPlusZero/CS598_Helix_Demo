import os
import sys

def generate_template(workflow):
    res = ""
    res += "object %s extends Workflow {\n" % (workflow)
    res += "  override def declare_sources: Unit = {}\n"
    res += "  override def declare_scanners: Unit = {}\n"
    res += "  override def declare_extractors: Unit = {}\n"
    res += "  override def declare_example_makers: Unit = {}\n"
    res += "  override def declare_classifiers: Unit = {}\n"
    res += "  override def declare_learning: Unit = {}\n"
    res += "  override def declare_output: Unit = {}\n"
    res += '  def main(args: Array[String]) = {\n'
    res += '    this.setProperty("data_loc", "input/all.data")\n'
    res += '    this.setProperty("outputDir", "example_output")\n'
    res += '    driver_main(args)\n'
    res += '  }'
    res += "}\n"
    return res

def code_fillup(mlcode):
    header = 'package com.smiley.datamodel.workflows.client\nimport com.smiley.datamodel.driver.Driver._\nimport com.smiley.datamodel.example.Example\nimport com.smiley.datamodel.feature.Extractor\nimport com.smiley.datamodel.learner.{FeatureVectorLearner, Reducer}\nimport com.smiley.datamodel.reader.source.SomeSource\nimport com.smiley.datamodel.reader.{RowScanner, Scanner, Workflow}\nimport org.apache.spark.rdd.RDD\n'
    return header + mlcode