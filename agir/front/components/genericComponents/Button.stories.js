import React from "react";

import Button from "./Button";
import { allIcons } from "./FeatherIcon";

export default {
  component: Button,
  title: "Generic/Button",
  argTypes: {
    color: {
      control: {
        type: "select",
        options: Button.colors,
      },
    },
    icon: {
      name: "Nom de l'icône",
      control: {
        type: "select",
        options: allIcons,
      },
    },
  },
};

const Template = (args) => <Button {...args} />;

export const Default = Template.bind({});
Default.args = { small: false, disabled: false, children: "Texte du bouton" };

export const PrimaryColor = Template.bind({});
PrimaryColor.args = {
  ...Default.args,
  color: "primary",
};

export const SecondaryColor = Template.bind({});
SecondaryColor.args = {
  ...Default.args,
  color: "secondary",
};

export const ConfirmedColor = Template.bind({});
ConfirmedColor.args = {
  ...Default.args,
  color: "confirmed",
};

export const Unavailable = Template.bind({});
Unavailable.args = { ...Default.args, color: "unavailable" };

export const SmallExample = Template.bind({});
SmallExample.args = { ...Default.args, small: true };

export const DisabledExample = Template.bind({});
DisabledExample.args = { ...Default.args, disabled: true };

export const LinkButton = Template.bind({});
LinkButton.args = {
  ...Default.args,
  as: "a",
};

export const IconButton = Template.bind({});
IconButton.args = {
  ...Default.args,
  icon: "copy",
};