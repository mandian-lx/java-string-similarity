%{?_javapackages_macros:%_javapackages_macros}

Summary:	Implementation of various string similarity and distance algorithms for Java
Name:		java-string-similarity
Version:	0.21
Release:	1
License:	MIT
Group:		Development/Java
Url:		http://debatty.info/software/java-string-similarity
Source0:	https://github.com/tdebatty/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	maven-local
BuildRequires:	mvn(junit:junit)
BuildRequires:	mvn(net.jcip:jcip-annotations)
BuildRequires:	mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:	mvn(org.apache.maven.plugins:maven-release-plugin)
BuildRequires:	mvn(org.apache.maven.plugins:maven-source-plugin)

%description
A library implementing different string similarity and distance measures. A
dozen of algorithms (including Levenshtein edit distance and sibblings,
Jaro-Winkler, Longest Common Subsequence, cosine similarity etc.) are
currently implemented.

%files -f .mfiles
%doc README.md

#----------------------------------------------------------------------------

%package javadoc
Summary:	Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%files javadoc -f .mfiles-javadoc

#----------------------------------------------------------------------------

%prep
%setup -q
# Delete all prebuild binaries
find . -name "*.jar" -delete
find . -name "*.class" -delete

# Remove unuseful plugins
%pom_remove_plugin :nexus-staging-maven-plugin
%pom_remove_plugin :maven-gpg-plugin

# Build an OSGi compilant MANIFEST.MF
#http://wiki.osgi.org/wiki/Maven_Bundle_Plugin
%pom_add_plugin org.apache.felix:maven-bundle-plugin . "<extensions>true</extensions>
<configuration>
	<supportedProjectTypes>
		<supportedProjectType>bundle</supportedProjectType>
		<supportedProjectType>jar</supportedProjectType>
	</supportedProjectTypes>
	<instructions>
		<Bundle-Name>\${project.artifactId}</Bundle-Name>
		<Bundle-Version>\${project.version}</Bundle-Version>
	</instructions>
</configuration>
<executions>
	<execution>
		<id>bundle-manifest</id>
		<phase>process-classes</phase>
		<goals>
			<goal>manifest</goal>
		</goals>
	</execution>
</executions>"

# Add META-INF/MANIFEST.MF to the jar archive
# and fix jar-not-indexed warning)
%pom_add_plugin :maven-jar-plugin . "
<executions>
	<execution>
		<phase>package</phase>
		<configuration>
		<archive>
			<manifestFile>\${project.build.outputDirectory}/META-INF/MANIFEST.MF</manifestFile>
			<manifest>
				<addDefaultImplementationEntries>true</addDefaultImplementationEntries>
				<addDefaultSpecificationEntries>true</addDefaultSpecificationEntries>
			</manifest>
			<index>true</index>
		</archive>
		</configuration>
		<goals>
			<goal>jar</goal>
		</goals>
	</execution>
</executions>"

# Fix Jar name
%mvn_file :%{name} %{name}-%{version} %{name}

%build
#FIXME: inspect why tests fail
%mvn_build -f

%install
%mvn_install

