import PropTypes from "prop-types";
import React from "react";
import styled from "styled-components";

import FeatherIcon, {
  RawFeatherIcon,
} from "@agir/front/genericComponents/FeatherIcon";
import style from "@agir/front/genericComponents/_variables.scss";
import { useGlobalContext } from "@agir/front/genericComponents/GobalContext";

import CONFIG from "@agir/front/dashboardComponents/navigation.config";

const BottomBar = styled.nav`
  @media only screen and (max-width: ${style.collapse}px) {
    background-color: ${style.white};
    position: fixed;
    bottom: 0px;
    left: 0px;
    right: 0px;
    box-shadow: inset 0px 1px 0px #eeeeee;
    height: 72px;
    padding: 0 7%;
  }
`;

const Menu = styled.ul`
  @media only screen and (max-width: ${style.collapse}px) {
    padding: 0;
    max-width: 600px;
    margin: auto;
    display: flex;
    justify-content: space-between;
  }
`;

const MenuItem = styled.li`
  font-size: 16px;
  font-weight: 600;
  display: block;
  position: relative;

  & a {
    color: inherit;
    text-decoration: none;
  }

  ${(props) =>
    props.active &&
    `
    color: ${style.primary500};
    `}

  @media only screen and (max-width: ${style.collapse}px) {
    display: ${({ mobile }) => (mobile ? "flex" : "none")};
    width: 70px;
    height: 70px;
    flex-direction: column;
    justify-content: center;
    text-align: center;
    font-size: 11px;

    & ${RawFeatherIcon} {
      display: block;
    }
    ${(props) =>
      props.active &&
      `
    border-top: 2px solid ${style.primary500};
    `}
  }

  @media only screen and (min-width: ${style.collapse}px) {
    display: ${({ desktop }) => (desktop ? "flex" : "none")};
    line-height: 24px;
    align-items: center;
    margin-bottom: 1.5rem;

    & ${RawFeatherIcon} {
      color: ${(props) => (props.active ? style.primary500 : style.black500)};
      margin-right: 1rem;
    }

    ${RawFeatherIcon}:last-child {
      margin-right: 0;
      margin-left: 0.5rem;
    }
  }
`;

const SecondaryMenu = styled.ul`
  margin-top: 40px;
  display: flex;
  flex-flow: column nowrap;
  list-style: none;

  @media only screen and (max-width: ${style.collapse}px) {
    display: none;
  }
`;

const SecondaryMenuItem = styled.li`
  font-size: 12px;
  line-height: 15px;
  color: ${style.black500};
  margin-bottom: 16px;
  font-weight: bold;

  & a,
  & a:hover,
  & a:focus,
  & a:active {
    font-size: 13px;
    font-weight: normal;
    line-height: 1.1;
    color: ${style.black700};
    margin-bottom: 12px;
  }
`;

const Counter = styled.span`
  text-align: center;
  position: absolute;
  background-color: ${style.secondary500};
  color: #fff;
  font-size: 9px;
  height: 16px;
  width: 16px;
  border-radius: 8px;
  z-index: 1000;
  line-height: 14px;

  @media only screen and (max-width: ${style.collapse}px) {
    top: 11px;
    right: 16px;
  }

  @media only screen and (min-width: ${style.collapse}px) {
    top: 0px;
    left: 14px;
  }
`;

const MenuLink = (props) => {
  const { href, icon, title, active, counter, external } = props;
  const linkProps = React.useMemo(
    () => ({
      target: external ? "_blank" : undefined,
      rel: external ? "noopener noreferrer" : undefined,
    }),
    [external]
  );
  return (
    <MenuItem {...props} active={active}>
      <a {...linkProps} href={href}>
        {counter > 0 && <Counter>{counter}</Counter>}
        <FeatherIcon name={icon} inline />
        <span>{title}</span>
        {external && <FeatherIcon name="external-link" inline small />}
      </a>
    </MenuItem>
  );
};
MenuLink.propTypes = {
  href: PropTypes.string,
  icon: PropTypes.string,
  title: PropTypes.string,
  active: PropTypes.bool,
  counter: PropTypes.number,
  external: PropTypes.bool,
};

const Navigation = ({ active }) => {
  const { requiredActionActivities = [], routes } = useGlobalContext();
  return (
    <BottomBar>
      <Menu>
        {CONFIG.menuLinks.map((link) => (
          <MenuLink
            {...link}
            key={link.id}
            active={active === link.id}
            href={link.href || routes[link.route]}
            counter={link.counter && requiredActionActivities.length}
          />
        ))}
      </Menu>
      <SecondaryMenu>
        <SecondaryMenuItem key="title">LIENS</SecondaryMenuItem>
        {CONFIG.secondaryLinks.map((link) => (
          <SecondaryMenuItem key={link.id}>
            <a
              href={link.href || routes[link.route]}
              target="_blank"
              rel="noopener noreferrer"
            >
              {link.title}
            </a>
          </SecondaryMenuItem>
        ))}
      </SecondaryMenu>
    </BottomBar>
  );
};

export default Navigation;

Navigation.propTypes = {
  active: PropTypes.oneOf(["events", "groups", "activity", "menu"]),
};
