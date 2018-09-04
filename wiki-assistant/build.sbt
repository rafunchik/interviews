val Http4sVersion = "0.18.14"
val Specs2Version = "4.2.0"
val LogbackVersion = "1.2.3"

scalacOptions += "-Ypartial-unification" // 2.11.9+

lazy val root = (project in file("."))
  .settings(
    organization := "rcastro",
    name := "wiki-assistant",
    version := "0.0.1-SNAPSHOT",
    scalaVersion := "2.12.6",
    libraryDependencies ++= Seq(
      "org.postgresql"  % "postgresql"           % "9.3-1100-jdbc4",
      "com.typesafe.slick" %% "slick"            % "2.1.0",
      "org.http4s"      %% "http4s-blaze-server" % Http4sVersion,
      "org.http4s"      %% "http4s-circe"        % Http4sVersion,
      "org.http4s"      %% "http4s-dsl"          % Http4sVersion,
      "ch.qos.logback"  %  "logback-classic"     % LogbackVersion,
      "org.specs2"      %% "specs2-core"         % Specs2Version % "test",
      "org.specs2"      %% "specs2-analysis"     % Specs2Version % "test",
      "org.specs2"      %% "specs2-mock"         % Specs2Version % "test",
      "org.http4s"      %% "http4s-twirl"        % Http4sVersion,
      "org.tpolecat" %% "doobie-core"      % "0.5.3",
      "org.tpolecat" %% "doobie-postgres"  % "0.5.3", // Postgres driver 42.2.2 + type mappings.
      "org.tpolecat" %% "doobie-specs2"    % "0.5.3", // Specs2 support for typechecking statements.
      "org.tpolecat" %% "doobie-scalatest" % "0.5.3",  // ScalaTest support for typechecking statements.
      "mysql" % "mysql-connector-java" % "5.1.34"
)
  )

mainClass in assembly := Some("rcastro.wikiassistant.HelloWorldServer")
test in assembly := {}

addCompilerPlugin("org.scalamacros" % "paradise" % "2.1.0" cross CrossVersion.full)
