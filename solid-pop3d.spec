# Conditional build:
# _with_whoson - build wiht whoson support

Summary:	POP3 server
Summary(pl):	Serwer POP3
Name:		solid-pop3d
Version:	0.16d
Release:	4
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Vendor:		Jerzy Balamut <jurekb@dione.ids.pl>
URL:		http://solidpop3d.pld.org.pl/
Source0:	ftp://dione.ids.pl/pub/solidpop3d/%{name}-%{version}.tar.gz
Source1:	%{name}.conf
Source2:	%{name}-ssl.conf
Source3:	%{name}.inetd
Source4:	%{name}-ssl.inetd
Source5:	%{name}.pamd
Patch0:		%{name}-whoson2.patch
Provides:	pop3daemon
Prereq:		rc-inetd >= 0.8.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	pop3daemon
Obsoletes:	qpopper
Obsoletes:	qpopper6
Obsoletes:	imap-pop
Obsoletes:	solid-pop3d-ssl
BuildRequires:	gdbm-devel
BuildRequires:	openssl-devel >= 0.9.6a
%{?_with_whoson:BuildRequires: whoson-devel}
%define		_sysconfdir	/etc

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
%{?_with_whoson:%patch0 -p1}
%build
autoconf
%configure \
	--localstatedir=/var/mail \
	--enable-apop \
	--enable-pam \
	--enable-mailbox \
	--enable-maildir \
	--enable-bulletins \
	--enable-expire \
	--enable-configfile \
	--enable-userconfig \
	--enable-last \
	--enable-createmail \
	--enable-ipv6 \
	--enable-mapping \
	--enable-nonip \
	--enable-statistics \
	--enable-dpuid \
	--enable-logextend \
	--enable-userpasswd \
	--enable-authonly \
	--with-openssl \
	%{?_with_whoson: --enable-whoson} \
	--with-sasl
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{pam.d,sysconfig/rc-inetd,security} \
	$RPM_BUILD_ROOT/var/mail/bulletins

%{__make} install DESTDIR=$RPM_BUILD_ROOT 

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/spop3d.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/spop3d-ssl.conf
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/rc-inetd/spop3d
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/rc-inetd/spop3d-ssl
install %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/spop3d

gzip -9nf AUTHORS README THANKS VIRTUALS doc/config.example

touch $RPM_BUILD_ROOT%{_sysconfdir}/security/blacklist.spop3d

%pre
if [ -z "`id -u spop3d 2>/dev/null`" ]; then
	%{_sbindir}/useradd -u 70 -r -d /var/mail/bulletins -s /bin/false -c "Solid POP3 User" -g nobody spop3d 1>&2
fi

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
fi

if [ "$1" = "0" ]; then
	if [ -n "`id -u spop3d 2>/dev/null`" ]; then
		%{_sbindir}/userdel spop3d
	fi
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {AUTHORS,README,THANKS,VIRTUALS,doc/config.example}.gz
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_bindir}/*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/rc-inetd/spop3d
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/rc-inetd/spop3d-ssl
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/security/blacklist.spop3d
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pam.d/spop3d
%attr(640,spop3d,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/spop3d.conf
%attr(640,spop3d,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/spop3d-ssl.conf
%attr(755,root,root) %dir /var/mail/bulletins
%{_mandir}/man[158]/*
