import { Stack } from 'expo-router';
import * as React from 'react';
import { View, Pressable } from 'react-native';
import { Icon } from '@roninoss/icons';

import { Container } from '~/components/Container';
import { Text } from '~/components/nativewindui/Text';
import { useColorScheme } from '~/lib/useColorScheme';

// Mock data structure for accounts
type AccountTransaction = {
  id: string;
  selected?: boolean;
  account: string;
  date: string;
  payee: string;
  category: string;
  memo: string;
  outflow?: number;
  inflow?: number;
  cleared: boolean;
};

// Mock data
const mockTransactions: AccountTransaction[] = [
  {
    id: '1',
    account: 'Itau Cartão',
    date: '18/02/2025',
    payee: 'Manual Balance Adjustment',
    category: 'Inflow: Ready to Assign',
    memo: '',
    inflow: 14539.58,
    cleared: true,
  },
  // Add more mock transactions as needed
];

export default function Accounts() {
  const { colors } = useColorScheme();
  const [transactions, setTransactions] = React.useState(mockTransactions);

  const toggleSelection = (id: string) => {
    setTransactions(prev =>
      prev.map(t =>
        t.id === id ? { ...t, selected: !t.selected } : t
      )
    );
  };

  return (
    <>
      <Stack.Screen options={{ title: 'Accounts' }} />
      <Container>
        <View className="flex-1">
          {/* Table Header */}
          <View className="flex-row items-center border-b border-border bg-card p-4">
            <View className="w-8" />
            <Text className="w-32 font-medium">Account</Text>
            <Text className="w-24 font-medium">Date</Text>
            <Text className="w-48 font-medium">Payee</Text>
            <Text className="flex-1 font-medium">Category</Text>
            <Text className="w-32 font-medium">Memo</Text>
            <Text className="w-24 font-medium text-right">Outflow</Text>
            <Text className="w-24 font-medium text-right">Inflow</Text>
            <View className="w-8" />
          </View>

          {/* Table Content */}
          {transactions.map((transaction) => (
            <View
              key={transaction.id}
              className="flex-row items-center border-b border-border p-4 hover:bg-muted/50">
              <Pressable
                onPress={() => toggleSelection(transaction.id)}
                className="w-8 items-center">
                <View className={`h-4 w-4 rounded border border-border ${transaction.selected ? 'bg-primary' : 'bg-transparent'}`} />
              </Pressable>
              <Text className="w-32" color="secondary">
                {transaction.account}
              </Text>
              <Text className="w-24" color="secondary">
                {transaction.date}
              </Text>
              <Text className="w-48" color="secondary">
                {transaction.payee}
              </Text>
              <Text className="flex-1" color="secondary">
                {transaction.category}
              </Text>
              <Text className="w-32" color="secondary">
                {transaction.memo}
              </Text>
              <Text className="w-24 text-right" color="secondary">
                {transaction.outflow ? `R$${transaction.outflow.toFixed(2)}` : ''}
              </Text>
              <Text className="w-24 text-right" color="green">
                {transaction.inflow ? `R$${transaction.inflow.toFixed(2)}` : ''}
              </Text>
              <View className="w-8 items-center">
                {transaction.cleared && (
                  <Icon name="check-circle" size={16} color={colors.green} />
                )}
              </View>
            </View>
          ))}
        </View>
      </Container>
    </>
  );
} 