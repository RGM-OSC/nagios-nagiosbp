%define realname	nagios-business-process-addon

Name: nagiosbp
Version: 0.9.6
Release: 11.rgm
Summary: Nagios business process addon

Group: Applications/System
License: GPL
URL: http://nagiosbp.projects.nagiosforge.org/
Source0: %{realname}.tar.gz
Source1: language_pack_fr.tar.gz
Source2: %{name}-rgm.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

Requires: rgm-base, nagios, mk-livestatus, perl > 5.8, perl-CGI-Simple, perl-libwww-perl
BuildRequires: rpm-macros-rgm


# define path
%define datadir		%{rgm_path}/%{name}-%{version}
%define linkdir		%{rgm_path}/%{name}

%define rgmlibdir       %{_sharedstatedir}/rgm/%{name}

%description
The AddOn Business Process View takes results of the single nagios checks out of NDO (Nagios' database) and builds up aggregated states.

%prep
%setup -T -b 0 -n %{realname}
%setup -T -b 1 -n language_pack_fr
%setup -T -b 2 -n %{name}-rgm

%build
cd ../%{realname}
export PATH=$PATH:/usr/sbin
CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" \
./configure \
	--datadir=%{datadir}/share \
	--with-nagiosbp-user=%{rgm_user_nagios} \
	--with-nagiosbp-group=%{rgm_group} \
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
install -D -m 0755 %{realname}/bin/*.pl %{buildroot}%{datadir}/bin/
install -D -m 0755 %{realname}/bin/nagios_bp_session_timeout %{buildroot}%{datadir}/bin/
install -d -m 0755 %{buildroot}%{datadir}/etc
install -D -m 0644 %{realname}/etc/cron.d/%{name} %{buildroot}%{_sysconfdir}/cron.d 
install -d -m 0755 %{buildroot}%{datadir}/lib
install -D -m 0644 %{realname}/lib/*.pm %{buildroot}%{datadir}/lib/
install -d -m 0755 %{buildroot}%{datadir}/libexec
install -D -m 0755 %{realname}/libexec/check_bp_status.pl %{buildroot}%{datadir}/libexec/
install -d -m 0755 %{buildroot}%{datadir}/sbin
install -D -m 0755 %{realname}/sbin/nagios-bp.cgi %{buildroot}%{datadir}/sbin/
install -D -m 0755 %{realname}/sbin/whereUsed.cgi %{buildroot}%{datadir}/sbin/
install -d -m 0755 %{buildroot}%{datadir}/share/lang
install -d -m 0755 %{buildroot}%{datadir}/share/stylesheets
install -D -m 0644 %{realname}/share/*.gif %{buildroot}%{datadir}/share/
install -D -m 0644 %{realname}/share/lang/*.txt %{buildroot}%{datadir}/share/lang/
install -D -m 0644 %{realname}/share/stylesheets/nagios-bp.css %{buildroot}%{datadir}/share/stylesheets/nagios-bp.css
install -d -m 0775 %{buildroot}%{datadir}/var/nagios_bp.sessions

# language fr file
install -D -m 0644 language_pack_fr/i18n_fr.txt %{buildroot}%{datadir}/share/lang/

# rgm specifics
install -D -m 0664 %{name}-rgm/nagios-bp.conf %{buildroot}%{datadir}/etc/
install -D -m 0644 %{name}-rgm/ndo.cfg %{buildroot}%{datadir}/etc/
install -D -m 0644 %{name}-rgm/settings.cfg %{buildroot}%{datadir}/etc/
install -D -m 0644 %{name}-rgm/schema_nagiosbp.sql %{buildroot}%{datadir}/etc/
install -D -m 0644 %{name}-rgm/nagios-bp.css %{buildroot}%{datadir}/share/stylesheets/
install -D -m 0644 %{name}-rgm/user.css %{buildroot}%{datadir}/share/stylesheets/
install -d -m0755 %{buildroot}%{rgm_docdir}/httpd
install -D -m 0644 %{name}-rgm/httpd-nagiosbp.example.conf %{buildroot}%{rgm_docdir}/httpd/

# patch RGM path on settings.cfg
sed -i 's|/srv/rgm/|%{rgm_path}/|' %{buildroot}%{datadir}/etc/settings.cfg
# patch ndo.cfg
sed -i 's|/srv/rgm/|%{rgm_path}/|' %{buildroot}%{datadir}/etc/ndo.cfg
sed -i 's|rgminternal|%{rgm_sql_internal_user}|' %{buildroot}%{datadir}/etc/ndo.cfg
sed -i 's|0rd0-c0m1735-b47h0n143|%{rgm_sql_internal_pwd}|' %{buildroot}%{datadir}/etc/ndo.cfg


%post
ln -nsf %{datadir} %{linkdir}
chown -h %{rgm_user_nagios}:%{rgm_group} %{linkdir}
#chmod -R g+w %{datadir}/var/nagios_bp.sessions
if [ -e %{_sysconfdir}/httpd/conf.d/nagiosbp.conf ]; then
    rm -f %{_sysconfdir}/httpd/conf.d/nagiosbp.conf
fi
# execute SQL postinstall script
/usr/share/rgm/manage_sql.sh -d %{rgm_db_nagiosbp} -s %{datadir}/etc/schema_nagiosbp.sql -u %{rgm_sql_internal_user} -p %{rgm_sql_internal_pwd}


%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%{_sysconfdir}/cron.d/nagiosbp


%doc %{rgm_docdir}/httpd/httpd-nagiosbp.example.conf

%defattr(-, %{rgm_user_nagios}, %{rgm_group}, 0755)
%{datadir}
%config(noreplace) %{datadir}/etc/nagios-bp.conf

%defattr(0664, %{rgm_user_nagios}, %{rgm_group}, 0775)
%{datadir}/var/nagios_bp.sessions


%changelog

* Thu Mar 11 2021 Eric Belhomme <ebelhomme@fr.scc.com> - 0.9.6-11.rgm
- move httpd config file as example file in /usr/share/doc/rgm/httpd/

* Thu Sep 26 2019 Michael Aubertin <maubertin@fr.scc.com> - 0.9.6-10.rgm
- Fix initial BP

* Thu Sep 26 2019 Michael Aubertin <maubertin@fr.scc.com> - 0.9.6-9.rgm
- Initial RGM BP 

* Wed Apr 24 2019 Michael Aubertin <maubertin@fr.scc.com> - 0.9.6-8.rgm
- Harmonize theme 

* Wed Apr 24 2019 Michael Aubertin <maubertin@fr.scc.com> - 0.9.6-7.rgm
- Harmonize theme 

* Wed Apr 24 2019 Michael Aubertin <maubertin@fr.scc.com> - 0.9.6-6.rgm
- Harmonize theme 

* Fri Apr 12 2019 Michael Aubertin <maubertin@fr.scc.com> - 0.9.6-5.rgm
- Fix themes and dep 

* Thu Mar 14 2019 Eric Belhomme <ebelhomme@fr.scc.com> - 0.9.6-4.rgm
- add rpm-macros-rgm as build dependency
- add rgm-base as dependency
- add SQL schema creation script
- fix RGM paths and SQL creds on config files 

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

* Tue Nov 18 2008 Jean-Philippe Levy <jeanphilippe.levy@gmail.com> - 0.9.2-0.eon
- packaged for EyesOfNetwork appliance
