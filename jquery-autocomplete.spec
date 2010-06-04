%define		plugin	autocomplete
Summary:	jQuery plugin: Autocomplete
Name:		jquery-%{plugin}
Version:	1.1
Release:	2
License:	MIT / GPL v2
Group:		Applications/WWW
Source0:	http://jquery.bassistance.de/autocomplete/jquery.autocomplete.zip
# Source0-md5:	7de19c33f0c08f20cc5e496eb10787f0
URL:		http://bassistance.de/jquery-plugins/jquery-plugin-autocomplete/
BuildRequires:	js
BuildRequires:	rpmbuild(macros) >= 1.565
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
BuildRequires:	yuicompressor
Requires:	jquery >= 1.2.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir	%{_datadir}/jquery/%{plugin}

%description
Autocomplete an input field to enable users quickly finding and
selecting some value, leveraging searching and filtering.

By giving an autocompleted field focus or entering something into it,
the plugin starts searching for matching entries and displays a list
of values to choose from. By entering more characters, the user can
filter down the list to better matches.

This can be used to enter previous selected values, eg. for tags, to
complete an address, eg. enter a city name and get the zip code, or
maybe enter email addresses from an addressbook.

%package demo
Summary:	Demo for jQuery.autocomplete
Group:		Development
Requires:	%{name} = %{version}-%{release}
Requires:	jquery-thickbox

%description demo
Demonstrations and samples for jQuery.autocomplete.

%prep
%setup -qn %{name}
%undos changelog.txt todo

# avoid filename conflict
sed -i -e '
	s,indicator.gif,jquery.autocomplete-indicator.gif,
' jquery.autocomplete.css

cd demo
%undos -f html,js,css

sed -i -e '
	s,../lib/jquery.js,jquery/jquery.js,

	s,../jquery.autocomplete.js,jquery/autocomplete/autocomplete.js,
	s,../jquery.autocomplete.css,jquery/autocomplete/autocomplete.css,

	s,../lib/thickbox.css,jquery/thickbox/thickbox.css,
	s,../lib/thickbox-compressed.js,jquery/thickbox/thickbox.js,
' index.html json.html

ln -s %{_datadir}/jquery .

%build
install -d build

# compress .js
yuicompressor --charset UTF-8 jquery.autocomplete.min.js -o build/autocomplete.js
js -C -f build/autocomplete.js

# compress with yui to get rid of comments, etc
yuicompressor --charset UTF-8 jquery.autocomplete.css -o build/autocomplete.css

# used by css
cp -a demo/indicator.gif build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_examplesdir}/%{name}-%{version}}
cp -a build/* $RPM_BUILD_ROOT%{_appdir}
cp -a demo/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc changelog.txt todo
%{_appdir}

%files demo
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
