%define realname	nagios-business-process-addon

Name: nagiosbp
Version: 0.9.6
Release: 3.rgm
Summary: Nagios business process addon

Group: Applications/System
License: GPL
URL: http://nagiosbp.projects.nagiosforge.org/
Source0: %{realname}-%{version}.tar.gz
Source1: language_pack_fr_%{version}.tar.gz
Source2: %{name}-rgm.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

Requires: nagios, mk-livestatus, perl > 5.8, perl-CGI-Simple

# define path
%define rgmdir		/srv/rgm
%define rgmconfdir	/srv/eyesofnetworkconf/%{name}
%define datadir		%{rgmdir}/%{name}-%{version}
%define linkdir		%{rgmdir}/%{name}

# define user / group
%define NAGIOSUSR	nagios
%define APPLIANCEGRP	rgm

%description
The AddOn Business Process View takes results of the single nagios checks out of NDO (Nagios' database) and builds up aggregated states.

%prep
%setup -T -b 0 -n %{realname}-%{version}
%setup -T -b 1 -n fr
%setup -T -b 2 -n %{name}-rgm

%build
cd ../%{realname}-%{version}
export PATH=$PATH:/usr/sbin
CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" \
./configure \
 	--datadir=%{datadir}/share \
	--with-nagiosbp-user=%{NAGIOSUSR} \
	--with-nagiosbp-group=%{APPLIANCEGRP} \
	--with-nagetc=%{rgmdir}/nagios/etc  \
	--with-naghtmurl=/nagios \
	--with-nagcgiurl=/thruk/cgi-bin \
	--with-cron-d-dir=%{_sysconfdir}/cron.d \
	--prefix=%{datadir}

%install
cd ..
install -d -m 0755 %{buildroot}%{_sysconfdir}/cron.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/httpd/conf.d
install -d -m 0755 %{buildroot}%{datadir}/bin
install -D -m 0755 %{realname}-%{version}/bin/*.pl %{buildroot}%{datadir}/bin/
install -D -m 0755 %{realname}-%{version}/bin/nagios_bp_session_timeout %{buildroot}%{datadir}/bin/
install -d -m 0755 %{buildroot}%{datadir}/etc
install -D -m 0644 %{realname}-%{version}/etc/cron.d/%{name} %{buildroot}%{_sysconfdir}/cron.d 
install -d -m 0755 %{buildroot}%{datadir}/lib
install -D -m 0644 %{realname}-%{version}/lib/*.pm %{buildroot}%{datadir}/lib/
install -d -m 0755 %{buildroot}%{datadir}/libexec
install -D -m 0755 %{realname}-%{version}/libexec/check_bp_status.pl %{buildroot}%{datadir}/libexec/
install -d -m 0755 %{buildroot}%{datadir}/sbin
install -D -m 0755 %{realname}-%{version}/sbin/nagios-bp.cgi %{buildroot}%{datadir}/sbin/
install -D -m 0755 %{realname}-%{version}/sbin/whereUsed.cgi %{buildroot}%{datadir}/sbin/
install -d -m 0755 %{buildroot}%{datadir}/share/lang
install -d -m 0755 %{buildroot}%{datadir}/share/stylesheets
install -D -m 0644 %{realname}-%{version}/share/*.gif %{buildroot}%{datadir}/share/
install -D -m 0644 %{realname}-%{version}/share/lang/*.txt %{buildroot}%{datadir}/share/lang/
install -D -m 0644 %{realname}-%{version}/share/stylesheets/nagios-bp.css %{buildroot}%{datadir}/share/stylesheets/nagios-bp.css
install -d -m 0775 %{buildroot}%{datadir}/var/nagios_bp.sessions

# language fr file
install -D -m 0644 fr/i18n_fr.txt %{buildroot}%{datadir}/share/lang/

# rgm specifics
install -D -m 0664 %{name}-rgm/nagios-bp.conf %{buildroot}%{datadir}/etc/
install -D -m 0644 %{name}-rgm/ndo.cfg %{buildroot}%{datadir}/etc/
install -D -m 0644 %{name}-rgm/settings.cfg %{buildroot}%{datadir}/etc/
install -D -m 0644 %{name}-rgm/nagios-bp.css %{buildroot}%{datadir}/share/stylesheets/
install -D -m 0644 %{name}-rgm/user.css %{buildroot}%{datadir}/share/stylesheets/
install -D -m 0644 %{name}-rgm/%{name}.conf %{buildroot}/%{_sysconfdir}/httpd/conf.d/%{name}.conf

%post
ln -nsf %{datadir} %{linkdir}
chown -h %{NAGIOSUSR}:%{APPLIANCEGRP} %{linkdir}
chmod -R g+w %{datadir}/var/nagios_bp.sessions

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%{_sysconfdir}/cron.d/nagiosbp
%{_sysconfdir}/httpd/conf.d/nagiosbp.conf
%defattr(-, %{NAGIOSUSR}, %{APPLIANCEGRP}, 0755)
%{datadir}
%config(noreplace) %{datadir}/etc/nagios-bp.conf

%changelog
* Fri Feb 22 2019 Michael Aubertin <maubertin@fr.scc.com> - 0.9.6-3.rgm
- Initial fork

* Thu Jun 20 2013 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 0.9.6-3.eon
- packaged for EyesOfNetwork appliance 4.0
- set default language "en" instead of "de" fix

* Wed Mar 06 2013 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 0.9.6-2.eon
- keep configuration file on update fix

* Thu Aug 23 2012 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 0.9.6-1.eon
- thruk cgi url fix

* Sun Oct 24 2010 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 0.9.6-0.eon
- packaged for EyesOfNetwork appliance 2.2

* Wed Jul 28 2010 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 0.9.5-1.eon
- packaged for EyesOfNetwork appliance 2.2

* Thu Mar 11 2010 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 0.9.5-0.eon
- packaged for EyesOfNetwork appliance 2.1

* Fri Oct 30 2009 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 0.9.4-0.eon
- packaged for EyesOfNetwork appliance 2.0

* Wed Jul 10 2009 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 0.9.3-0.eon
- packaged for EyesOfNetwork appliance 2.0

* Thu Nov 18 2008 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 0.9.2-0.eon
- packaged for EyesOfNetwork appliance
