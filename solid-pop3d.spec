Summary:	POP3 server
Summary(pl):	Serwer POP3
Name:		solid-pop3d
Version:	0.12
Release:	1
License:	GPL
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Vendor:		Jerzy Balamut <jurekb@dione.ids.pl>
Source:		ftp://dione.ids.pl/pub/solidpop3d/%{name}-%{version}.tar.gz
Source1:	%{name}.conf
Source2:	%{name}.inetd
Source3:	%{name}.pamd
Buildroot:	/tmp/%{name}-%{version}-root
Prereq:		rc-inetd >= 0.8.1

%define _sysconfdir	/etc

%description
The Solid POP3 Server is an implementation of a Post Office Protocol
version 3 server that has flexibility as its main goal. The server is
easily configurable and has support for few features such as:
- APOP authentication scheme
- virtual hosting
- maildir and mailbox handling
- bulletins
- expiration of messages

%description -l pl
Serwer Solid POP3 jest implementacj± protoko³u Post Office Protocol w
wersji 3 maj±cy za g³ówny cel elastyczno¶æ. Serwer jest ³atwo
konfigurowalny oraz posiada wsparcie dla wielu nowinek takich jak:
- schemat autoryzacji APOP
- wirtualne serwery
- formaty maildir oraz mailbox skrzynek pocztowych
- obs³uga biuletynów
- obs³uga przeterminowywania siê wiadomo¶ci

%prep
%setup -q

%build
autoconf
LDFLAGS="-s"; export LDFLAGS
%configure \
	--localstatedir=/var/mail \
	--enable-pam \
	--enable-apop \
	--enable-mailbox \
	--enable-maildir \
	--enable-bulletins \
	--enable-expire \
	--enable-configfile \
	--enable-userconfig \
	--enable-last \
	--enable-createmail \
	--enable-ipv6
make

%install
rm -rf	$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/{pam.d,sysconfig/rc-inetd,security}
install -d $RPM_BUILD_ROOT/var/mail/bulletins
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/spop3d.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/rc-inetd/spop3d
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/spop3d

make install DESTDIR=$RPM_BUILD_ROOT 

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* \
	  AUTHORS README THANKS VIRTUALS doc/config.example

touch $RPM_BUILD_ROOT%{_sysconfdir}/security/blacklist.spop3d

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet sever" 1>&2
fi

%postun
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd stop
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {AUTHORS,README,THANKS,VIRTUALS,doc/config.example}.gz
%attr(755,root,root) %{_sbindir}/spop3d
%attr(755,root,root) %{_bindir}/pop_auth
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/rc-inetd/spop3d
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/security/blacklist.spop3d
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pam.d/spop3d
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/spop3d.conf
%attr(755,root,root) %dir /var/mail/bulletins
%{_mandir}/man[158]/*
