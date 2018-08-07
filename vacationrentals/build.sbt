val Http4sVersion = "0.18.14"
val Specs2Version = "4.2.0"
val LogbackVersion = "1.2.3"
val CirceVersion = "0.9.3"

lazy val root = (project in file("."))
  .settings(
    organization := "com.example",
    name := "Listings",
    version := "0.0.1",
    scalaVersion := "2.11.12",
    libraryDependencies ++= Seq(
      "org.http4s"      %% "http4s-blaze-server" % Http4sVersion,
      "org.http4s"      %% "http4s-circe"        % Http4sVersion,
      "org.http4s"      %% "http4s-dsl"          % Http4sVersion,
      "io.circe"        %% "circe-literal"       % CirceVersion,
      "io.circe"        %% "circe-generic"       % CirceVersion,
      "io.circe"        %% "circe-generic-extras" % CirceVersion,
      "org.specs2"      %% "specs2-core"         % Specs2Version % "test",
      "org.specs2"      %% "specs2-analysis"     % Specs2Version % "test",
      "org.specs2"      %% "specs2-mock"         % Specs2Version % "test",
      "ch.qos.logback"  %  "logback-classic"     % LogbackVersion
    )
  )

addCompilerPlugin("org.scalamacros" % "paradise" % "2.1.0" cross CrossVersion.full)
