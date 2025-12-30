import All_Sunbeam_certified_courses as scraper

scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses/apache-spark-mastery-data-engineering-pyspark",
    "Apache Spark Mastery",
    "apache_spark_mastery.txt"
)

scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses/core-java-classes",
    "Core Java Classes",
    "core_java_classes.txt"
)

scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses/aptitude-course-in-pune",
    "Aptitude",
    "aptitude_course.txt"
)

scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses/data-structure-algorithms-using-java",
    "Data Structures and Algorithms",
    "data_structures_algorithms.txt"
)

scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses/Devops-training-institute",
    "DevOps",
    "devops.txt"
)

scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses/dreamllm-training-institute-pune",
    "Dream LLM",
    "dream_llm.txt"
)

scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses/machine-learning-classes",
    "Machine Learning",
    "machine_learning.txt"
)

scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses/mastering-generative-ai",
    "Mastering Generative AI",
    "mastering_gen_ai.txt"
)

scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses.php?mdid=57",
    "Mastering MCQs",
    "mastering_mcqs.txt"
)

scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses/mern-full-stack-developer-course",
    "MERN Full Stack Development",
    "mern_full_stack.txt"
)

scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses/mlops-llmops-training-institute-pune",
    "MLOps & LLMOps",
    "mlops_llmops.txt"
)

scraper.scrape_modular_courses(
    "https://sunbeaminfo.in/modular-courses/python-classes-in-pune",
    "Python Development",
    "python_development.txt"
)

print("\nAll course scraping completed")
