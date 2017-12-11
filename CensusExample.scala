object CensusExample extends Workflow {
  val data = "data"
  val columns = Scanner.getColumnNamesFromFile("./input/test_header.txt")
  val rows = "rows"

  // Feature names
  val age = "age" //continuous
  val workclass = "workclass"
  val fnlwgt = "fnlwgt" //continuous
  val fw_bkt = "fw-bkt"
  val age_bkt = "age-bucketize"
  val education = "education"
  val education_num = "education-num"  // continuous
  val marital_status = "marital-status"
  val occupation = "occupation"
  val relationship = "relationship"
  val race = "race"
  val gender = "gender"
  val capital_gain = "capital-gain"  // continuous
  val cg_bkt = "cg_bkt"
  val capital_loss = "capital-loss"  // continuous
  val cl_bkt = "cl_bkt"
  val hours_per_week = "hours-per-week"  // continuous
  val native_country = "native-country"

  val eduXoc = "eduXoc"
  val rXocXabkt = "rXocXabkt"
  val eXm = "eXm"

  val target = "target"
  val test_target = "test-target"

  val income = "income"
  val predictions = "predictions"
  val lean_example = "lean_example"
  val learned_output = "pred"
  val checkResults = "checkResults"
  val checked = "checked"

  val cls = "cls"

  /////// Experimental parameters ///////
  val data_loc = "data_loc"

  val pUseContinuous = "useContinuous"
  val pUseCat = "useCat"
  val pUseBucket = "useBucket"
  val pUseInteract = "useInteract"

  val pRetrain = "retrain"
  val pScale = "scale"
  val pModelType = "modelType"

  val pRowReuse = "rowReuse"
  val pIncomeReuse = "incomeReuse"
  val plearnedReuse = "learnedReuse"

  val pPredOutput = "predOutput"

  val pCheckResults = "checkResults"

  override def declare_sources: Unit = {
    val dLoc = getProperty(data_loc)
    data refers_to new SomeSource[String](dLoc)
  }

  override def declare_scanners: Unit = {
    data is_read_into rows using RowScanner(columns, ",")
  }

  override def declare_extractors: Unit = {
    age refers_to Extractor.getFieldExtractor(age, isIntermediate = true)
    workclass refers_to Extractor.getFieldExtractor(workclass)
    education refers_to Extractor.getFieldExtractor(education)
    education_num refers_to Extractor.getFieldExtractor(education_num)
    marital_status refers_to Extractor.getFieldExtractor(marital_status)
    occupation refers_to Extractor.getFieldExtractor(occupation)
    relationship refers_to Extractor.getFieldExtractor(relationship)
    race refers_to Extractor.getFieldExtractor(race)
    gender refers_to Extractor.getFieldExtractor(gender)
    hours_per_week refers_to Extractor.getFieldExtractor(hours_per_week)
    native_country refers_to Extractor.getFieldExtractor(native_country)

    fnlwgt refers_to Extractor.getFieldExtractor(fnlwgt)
    fw_bkt refers_to Extractor.getBucketizer(fw_bkt, fnlwgt, numBuckets = 5)
    fw_bkt uses fnlwgt

    capital_gain refers_to Extractor.getFieldExtractor(capital_gain, isIntermediate = false)
    //cg_bkt refers_to Extractor.getBucketizer(cg_bkt, capital_gain, numBuckets = 5)
    //cg_bkt uses (capital_gain)

    capital_loss refers_to Extractor.getFieldExtractor(capital_loss, isIntermediate = false)
    //cl_bkt refers_to Extractor.getBucketizer(cl_bkt, capital_loss, numBuckets = 5)
    //cl_bkt uses (capital_loss)

    age_bkt refers_to Extractor.getBucketizer(age_bkt, age, boundaries = List(18, 88, 10))
    age_bkt uses age

    eduXoc refers_to Extractor.getInteraction(eduXoc, List(education, occupation))
    eduXoc uses (education, occupation)
    rXocXabkt refers_to Extractor.getInteraction(rXocXabkt, List(race, occupation, age_bkt))
    rXocXabkt uses (race, occupation, age_bkt)
    eXm refers_to Extractor.getInteraction(eXm, List(education, marital_status))
    eXm uses (education, marital_status)

    target refers_to Extractor.getFieldExtractor(target)
    test_target refers_to Extractor.getFieldExtractor(test_target)

    rows has_extractors(target, test_target)

    if (hasProperty(pUseCat) && getProperty(pUseCat).toBoolean) {
      rows has_extractors (workclass, education, marital_status, occupation,
        relationship, race, gender, native_country)
    }

    if (hasProperty(pUseInteract) && getProperty(pUseInteract).toBoolean) {
      rows has_extractors(eduXoc, rXocXabkt, eXm)
    }

    if (hasProperty(pUseContinuous) && getProperty(pUseContinuous).toBoolean) {
      rows has_extractors (age, fnlwgt, education_num, capital_gain, capital_loss, hours_per_week)
    }

    if (hasProperty(pUseBucket) && getProperty(pUseBucket).toBoolean) {
      rows has_extractors age_bkt
    }
  }

  override def declare_example_makers: Unit = {}

  override def declare_classifiers: Unit = {
    val overWrite = if (hasProperty(pRetrain)) getProperty(pRetrain).toBoolean else false
    val scaling = if (hasProperty(pScale)) getProperty(pScale).toBoolean else false
    val modelType = if (hasProperty(pModelType)) getProperty(pModelType) else FeatureVectorLearner.LRLBFGS

    cls refers_to new FeatureVectorLearner[Array[Example]](cls,
      location = "example_model", driver = driver,
      modelType = modelType, useScaling = scaling, dropWeightsBelow = 0.0)

    val func = (results: RDD[Example]) => {
      val filtered = results.filter(_.hasFeature("rows::test-target"))
      val counts = filtered.aggregate((0, 0))((u, obj) => {
        val correct = if (obj.hasFeature("rows::test-target")) {
          val v1 = obj.getLabel.value
          val v2 = obj.getFeature("rows::test-target").value
          v1 == v2
        } else false
        val acc = if (correct) u._2 + 1 else u._2
        (u._1 + 1, acc)
      }, (s, t) => (s._1 + t._1, s._2 + t._2))
      println(counts)
      println(s"Accuracy ${counts._2.toDouble / counts._1.toDouble}")
      counts
    }

    checkResults refers_to new Reducer[(Int, Int)](checkResults, func)
    checkResults uses ((rows, test_target))
  }

  override def declare_learning: Unit = {
    rows as_examples income with_labels target
    cls on income as_examples predictions
    //lean_example on learned as_examples learned_output
    checkResults on predictions as_examples checked
  }

  override def declare_output: Unit = {
    if (hasProperty(pRowReuse) && !getProperty(pRowReuse).toBoolean) {
      rows not_reusable()
    }
    if (hasProperty(pIncomeReuse) && !getProperty(pIncomeReuse).toBoolean) {
      income not_reusable()
    }
    if (hasProperty(plearnedReuse) && !getProperty(plearnedReuse).toBoolean) {
      predictions not_reusable()
    }

    if (hasProperty(pPredOutput) && getProperty(pPredOutput).toBoolean) {
      predictions is_output()
    }

    val runCheck = if (hasProperty(pCheckResults)) getProperty(pCheckResults).toBoolean else true
    if (runCheck) {
      checked is_output()
    }
  }

  def main(args: Array[String]) = {
    this.setProperty("data_loc", "input/all.data")
    this.setProperty("outputDir", "example_output")
    this.setProperty(pScale, "true")
    this.setProperty(pUseContinuous, "true")
    this.setProperty(pUseBucket, "true")
    this.setProperty(pUseCat, "true")
    this.setProperty(pUseInteract, "false")
    this.setProperty(MEASURE_MAP, "true")
    this.setProperty(pPredOutput, "true")
    driver_main(args)
  }
}
