Summary:	POP3 Server
Summary(pl):	Serwer POP3
Name:		solid-pop3d
Version:	0.12
Release:	1
Copyright:	GPL
Group:		System Environment/Daemons
Source:		ftp://dione.ids.pl/pub/solidpop3d/%{name}-%{version}.tar.gz
Vendor:		Jerzy Balamut <jurekb@dione.ids.pl>
Buildroot:	/tmp/%{name}-%{version}-root

%description
The Solid POP3 Server is an implementation of a Post Office Protocol version 3
server that has flexibility as its main goal. The server is easily
configurable and has support for few features such as:
- APOP authentication scheme
- virtual hosting
- maildir and mailbox handling
- bulletins
- expiration of messages

%description -l pl
Serwer Solid POP3 jest implementacj± protoko³u Post Office Protocol w wersji 3
maj±cy za g³ówny cel elastyczno¶æ. Serwer jest ³atwo konfigurowalny
oraz posiada wsparcie dla wielu nowinek takich jak:
- schemat autoryzacji APOP
- wirtualne serwery
- formaty maildir oraz mailbox skrzynek pocztowych
- obs³uga biuletynów
- obs³uga przeterminowywania siê wiadomo¶ci

%prep
%setup -q

%define _sysconfdir	/etc

%build
LDFLAGS="-s"; export LDFLAGS
%configure \
	--localstatedir=%{_localstatedir} \
	--sysconfdir=%{_sysconfdir} \
	--sbindir=%{_sbindir} \
	--mandir=%{_mandir} \
	--enable-pam \
	--enable-apop \
	--enable-mailbox \
	--enable-maildir \
	--enable-bulletins \
	--enable-expire \
	--enable-configfile \
	--enable-userconfig \
	--enable-last \
	--enable-ipv6
make

%install
rm -rf	$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/
install -d $RPM_BUILD_ROOT/%{_localstatedir}/bulletins/
install    doc/spop3d $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/

make install  \
	DESTDIR=$RPM_BUILD_ROOT 

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* \
	  AUTHORS README THANKS doc/config.example

%files
%defattr(644,root,root,755)
%doc AUTHORS.gz README.gz THANKS.gz doc/config.example.gz
%attr(755,root,root) %{_sbindir}/spop3d
%attr(755,root,root) %{_bindir}/pop_auth
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pam.d/spop3d
%attr(755,root,root) %dir %{_localstatedir}/bulletins
%attr(644,root,root) %{_mandir}/man[158]/*


%changelog
* Fri Dec 10 1999 Arkadiusz Miskiewicz <misiek@pld.org.pl>
- initial rpm release
